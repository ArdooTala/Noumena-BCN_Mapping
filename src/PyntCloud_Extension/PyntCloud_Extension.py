import pyntcloud
import pandas as pd
import numpy as np
import laspy


class VoxelgridCentersMeanSampler(pyntcloud.samplers.voxelgrid.VoxelgridSampler):
    """Returns the centroid of each group of points inside each occupied voxel."""

    def compute(self):
        df = self.pyntcloud.points.copy()
        df["voxel_n"] = self.voxelgrid.voxel_n
        df = df.iloc[:, 3:]
        df = df.groupby("voxel_n").mean()

        xyz_df = pd.DataFrame(
            np.c_[np.unique(self.voxelgrid.voxel_n),
                  self.voxelgrid.voxel_centers[np.unique(self.voxelgrid.voxel_n)]],
            columns=["vertex_n", "x", "y", "z"]
        ).set_index("vertex_n")

        xyz_df.index = xyz_df.index.map(int)

        result = pd.concat([xyz_df, df], axis=1, sort=False)
        return result


class PyntCloud_dev(pyntcloud.PyntCloud):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_sample(self, name, as_PyntCloud=False, **kwargs):
        if name == "voxelgrid_mean_centers":
            sampler = VoxelgridCentersMeanSampler(pyntcloud=self, **kwargs)
            sampler.extract_info()
            sample = sampler.compute()

            if as_PyntCloud:
                return self(sample)

            return sample
        else:
            return pyntcloud.PyntCloud.get_sample(self, name, as_PyntCloud, **kwargs)

    # def from_file(cls, filename, **kwargs):
    #     ext = filename.split(".")[-1].upper()
    #
    #     if ext.upper() == "LAS":
    #         """Read a .las/laz file and store elements in pandas DataFrame.
    #
    #             Parameters
    #             ----------
    #             filename: str
    #                 Path to the filename
    #             Returns
    #             -------
    #             data: dict
    #                 Elements as pandas DataFrames.
    #             """
    #         print("Overwriting the .LAS reading method . . .")
    #         if laspy is None:
    #             raise ImportError("laspy is needed for reading .las files.")
    #         data = {}
    #
    #         with laspy.file.File(filename, mode='rw') as las:
    #             data["points"] = pd.DataFrame(las.points["point"])
    #             data["points"].columns = (x.lower() for x in data["points"].columns)
    #             # because laspy do something strange with scale
    #             data["points"].loc[:, ["x", "y", "z"]] *= las.header.scale
    #             data["las_header"] = las.header
    #
    #         return cls(**data)
    #
    #     else:
    #         return pyntcloud.PyntCloud.from_file(filename, **kwargs)

    def filter_cloud(self, filter_channel, error_channel):
        self.points[filter_channel] *= 255.00 / (self.points[error_channel].astype('float64'))
