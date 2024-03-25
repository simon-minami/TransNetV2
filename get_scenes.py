'''
splits input video into scenes using info obtained from TransNetV2
input_video = path to unaltered video
txt_file = path to scenes.txt file generated by transnetv2.py
'''
import cv2
import os

def read_scene_boundaries(txt_file):
    scene_boundaries = []
    with open(txt_file, 'r') as f:
        for line in f:
            start, end = map(int, line.split())
            scene_boundaries.append((start, end))
    # scene_boundaries[0][0] = 1 # want the first scene to start at 1
    return scene_boundaries


def create_output_video(input_video, scene_boundaries):
    cap = cv2.VideoCapture(input_video)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter('videos/OREGON_WASHST_all_scenes.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 255, 0)  # Green color
    thickness = 2
    org = (10, 30)  # Position of the text (top left corner)


    for scene_idx, (start, end) in enumerate(scene_boundaries):
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)

        # TODO: uncomment if you want to remove the unnecessary camera angles
        # ret, frame = cap.read()
        # # Display the frame in a window so user can check if the camera angle is right
        # cv2.imshow('Frame', cv2.resize(frame, (700, 500)))
        # cv2.waitKey(1)
        # cv2.moveWindow('Frame', 0, 0)
        # print(f'frame start: {start}')
        #
        # loop = True
        # while loop:
        #     correct_angle = input('Is this the desired camera angle (y/n): ')
        #     if correct_angle == 'y':
        #         loop = False
        #     elif correct_angle == 'n':
        #         loop = False
        #     else:
        #         print('please input y/n')
        # if correct_angle == 'n':
        #     continue
        # cv2.destroyAllWindows()

        while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_FRAMES) <= end:
            ret, frame = cap.read()
            if ret:
                cv2.putText(frame, f'Scene: {scene_idx}', org, font, font_scale, font_color, thickness, cv2.LINE_AA)
                out.write(frame)
            else:
                break

    out.release()
    cap.release()

if __name__ == "__main__":
    input_video = 'videos/OREGON_WASHST_test.mp4'
    txt_file = 'videos/OREGON_WASHST_test.mp4.scenes.txt'

    scene_boundaries = read_scene_boundaries(txt_file)
    create_output_video(input_video, scene_boundaries)
