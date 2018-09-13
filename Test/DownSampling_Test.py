from src.PyntCloud_Extension.PyntCloud_Extension import PyntCloud_dev as pc
import pandas as pd
import os
import time

pd.set_option('display.max_columns', 500)


def main(path):
    for root, subs, files in os.walk(path):
        for file in files:
            t0 = time.time()
            if not file.endswith(".las"):
                continue
            print("_" * 50)
            print(os.path.join(root, file))

            cloud = pc.from_file(pc, os.path.join(root, file))

            print(cloud.points)
            # print(cloud.points.describe())

            voxelgrid_id = cloud.add_structure("voxelgrid", size_x=500, size_y=500, size_z=500)
            # print("Voxels added . . .")
            new_cloud = cloud.get_sample("voxelgrid_mean_centers",
                                         voxelgrid_id=voxelgrid_id,
                                         as_PyntCloud=False)
            # print(new_cloud)
            print("Saving . . .")
            new_cloud.to_csv("PointClouds/Exports/" + file[:-4] + "_Norm.csv")
            print("Done in {:.1f} seconds!\n".format(time.time() - t0))
            print("_" * 50)

    # #### Visualization: Proceed with caution, Heavy task.
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(new_cloud.points.iloc[:, 0],
    #            new_cloud.points.iloc[:, 1],
    #            new_cloud.points.iloc[:, 2],
    #            c=new_cloud.points.iloc[:, -3:].values/(256),
    #            s=1)

    # ax = fig.add_subplot(122, projection='3d')
    # ax.scatter(cloud.points.iloc[:, 0],
    #            cloud.points.iloc[:, 1],
    #            cloud.points.iloc[:, 2],
    #            c=cloud.points.iloc[:, -3:].values/(256),
    #            s=1)

    # plt.show()


if __name__ == "__main__":
    main("PointClouds/las/")
