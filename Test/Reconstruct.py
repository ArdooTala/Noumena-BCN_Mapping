import cv2
from src.colmapScripts.read_model import *


# ## Inputs to be set later: This was peice of main originally!
def recreate_sparse(imgs):
    cameras, images, points3D = \
        read_model(path='/Users/Ardoo/Desktop/COLMAP_Test/Exports/TXT0/',
                   ext=".txt")

    print("num_cameras:", len(cameras))
    print("num_images:", len(images))
    print("num_points3D:", len(points3D))
    print("\n\________(o_O)________/\n")

    point_cloud = {}
    for item in images.items():
        print('\n----{', item[0], '}-------------------------------------------------------------------------')
        print('File: {}'.format(item[1].name))

        imgData = imgs[item[1].name]
        img = imgData.collage
        print("Loaded and ready.\n\tResolution: {}\tData: {}"
              .format(img.shape, imgData.file))

        for i in range(len(item[1].point3D_ids)):
            pt3D = item[1].point3D_ids[i]
            if pt3D == -1:
                continue

            sparse_pt_pos = item[1].xys[i].astype(int)

            if imgData.maxX > sparse_pt_pos[0] > imgData.minX and \
                    imgData.maxY > sparse_pt_pos[1] > imgData.minY:
                sparse_pt_col = imgData.collage[sparse_pt_pos[0], sparse_pt_pos[1]]

                img = cv2.circle(img, (sparse_pt_pos[1], sparse_pt_pos[0]), 5, 0, 2)

                if pt3D not in list(point_cloud.keys()):
                    point_cloud[pt3D] = [sparse_pt_col, ]
                else:
                    point_cloud[pt3D].append(sparse_pt_col)

    with open("points3D.txt", 'w') as f:

        print("\nDrawing Thermal Points . . .")
        for item in point_cloud.items():
            loc = points3D[item[0]].xyz
            color = int(sum(item[1]) / len(item[1]))
            f.write("x{} y{} z{} col{}\n"
                    .format(loc[0], loc[1], loc[2], color))

        print("Drawing Undetected Points . . .\n")
        for p3Did in list(points3D.keys()):
            if p3Did not in list(point_cloud.keys()):
                loc = points3D[p3Did].xyz
                f.write("x{} y{} z{} col_\n"
                        .format(loc[0], loc[1], loc[2]))
                # ax.scatter(loc[0], loc[1], loc[2], s=1, c='g')
    print("Drawing Done.\n")

    # for item in point_cloud.items():
    #     print("\nPoint3D: {}\t\tValues: {} < {}\t[{}]"
    #           .format(item[0], min(item[1]), max(item[1]), item[1]))


if __name__ == '__main__':
    rgb_path = "/Volumes/Storage/COLMAP_Test/RGB_Big/GUI_Project/Dense/images/"
    trm_path = "/Volumes/Storage/COLMAP_Test/FLIR/"

    recreate_sparse(main(rgb_path, trm_path))
