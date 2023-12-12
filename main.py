import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient
from viam.components.camera import Camera
from viam.components.base import Base


async def connect():
    """
    Establishes a connection to the robot using credentials and options.

    Returns:
        RobotClient: Connected robot client.
    """
    creds = Credentials(
        type = 'robot-location-secret',
        payload = 'bjlx7g4cf89qw5joko6xjp9t5u1totjiw81ndkxishqrxwxw'
    )
    opts = RobotClient.Options(
        refresh_interval = 0,
        dial_options = DialOptions(credentials = creds)
    )
    return await RobotClient.at_address('hal-main.6n3fkdbbro.viam.cloud', opts)


async def spin_until_small_area(base, detector, spinRight, spinNum, vel, threshold_area):
    """
    Spin the robot in the specified direction until the largest detection area becomes smaller than the threshold.

    Args:
        direction (int): 1 for right, 0 for left.
        vel (int): Motor speed.
        threshold_area (int): Threshold area for stopping the spin.
    """
    while True:

        if spinRight == 1:
            print(f"Spinning right")
            await base.spin(-spinNum * 3, vel)
        else:
            print(f"Spinning left")
            await base.spin(spinNum * 3, vel)

        # Get detections from the captured frame
        detections = await detector.get_detections_from_camera("cam")

        if detections:
            # Find the largest detection
            largest_detection = max(detections, key=lambda d: (d.x_max - d.x_min) * (d.y_max - d.y_min))

            # Calculate the area of the largest detection
            largest_area = (largest_detection.x_max - largest_detection.x_min) * (largest_detection.y_max - largest_detection.y_min)

            print(f"We got area {largest_area}")
            if largest_area < threshold_area:
                print(f"Largest area is now smaller than {threshold_area} pixels. Stopping the spin.")
                break
        else:
            break

async def main():
    """
    Main function to control the robot's behavior based on object detection.
    """
    move_speed = 50
    spinNum = 10
    vel = 250
    threshold_area = 17000


    # Connect to robot client and set up components
    robot = await connect()
    base = Base.from_robot(robot, "viam_base")
    camera_name = "cam"
    camera = Camera.from_robot(robot, camera_name)
    frame = await camera.get_image(mime_type = "image/jpeg")

    # Grab the vision service for object detection
    my_detector = VisionClient.from_robot(robot, "my_green_detector")

    try:
        largest_area = -1
        largest_center = -1
        has_detect = False
        while True:
            # Capture a frame from the camera
            frame = await camera.get_image(mime_type="image/jpeg")

            # Get detections from the captured frame
            detections = await my_detector.get_detections_from_camera(camera_name)
            if detections:
                has_detect = True
                cur_largest = -1
                for detection in detections:
                    # Calculate the width and height of the detected object
                    width = detection.x_max - detection.x_min
                    height = detection.y_max - detection.y_min

                    # Calculate the area of the detected object
                    area = width * height

                    if area > cur_largest:
                        cur_largest = area
                        centerX = detection.x_min + detection.x_max / 2

                if cur_largest > largest_area:
                    print(f"Larger Area: {cur_largest} square pixels")
                    largest_area = cur_largest
                    largest_center = centerX
                else:
                    largest_area = -1
                    if centerX < frame.size[0] / 2:
                        await spin_until_small_area(base, my_detector, 1, spinNum, vel, threshold_area)
                    else:
                        await spin_until_small_area(base, my_detector, 0, spinNum, vel, threshold_area)
            elif has_detect:
                has_detect = False
                print(f"No dobject after detection. Spin by history")
                if largest_center < frame.size[0] / 2:
                    await spin_until_small_area(base, my_detector, 1, spinNum, vel, threshold_area)
                else:
                    await spin_until_small_area(base, my_detector, 0, spinNum, vel, threshold_area)

            # Move the robot straight (you might need to adjust the speed value)
            print(f"All Clear")
            await base.move_straight(move_speed, vel)

    except KeyboardInterrupt:
        pass
    finally:
        await robot.close()


if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")
