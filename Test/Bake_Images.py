import cv2
from multiprocessing import Pool, cpu_count, current_process
from src.colmapScripts.read_model import *
from src.NoumenaRobotics.ROI_Matching import ImageUtils


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(counter=0)
def mi(path):
    print("\n====Task#==[{:04}]=[{}]========================"
          .format(mi.counter, current_process().name))
    mi.counter += 1
    return ImageUtils(path)


def main(rgbs_path, thermals_path):
    ImageUtils.importThermalImages(thermals_path)

    for root, subs, files in os.walk(rgbs_path):
        paths = [(root, file) for file in files if file.endswith('.JPG')]
        print(">>> CPU cores available: %d" % cpu_count())

        # with Pool(cpu_count() - 1) as pool:
        #     print("~~~~ Into the pool ~~~~~~~~~~~~~~~~~~~~~~~~")
        #     imgLst = pool.map(mi, paths[:])
        #     print("And OUT!")

        imgLst = map(mi, paths[:])

        imgs = {imgUtl.file: imgUtl for imgUtl in imgLst}

        if not os.path.exists(os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")):
            os.makedirs(
                os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")
            )
        print("Saving filters to:\n\t{}"
              .format(os.path.join(os.path.dirname(rgbs_path[:-1]), "Filters")))

        ## Visualize the collages
        win = cv2.namedWindow("Good?")
        for i in imgs.values():
            if not hasattr(i, 'collage'):
                continue
            cv2.imshow(win, i.filter)
            cv2.imwrite(
                os.path.join(os.path.dirname(
                    rgbs_path[:-1]),
                    "Filters",
                    i.file),
                i.filter)
            # cv2.imshow(win, i.collage)
            # cv2.waitKey(1)

    assert imgs
    return imgs


if __name__ == '__main__':
    rgb_path = "/Volumes/STR-SSD/stealingfire/bcn-mapping/PT_5/dense-cloud-colmap/images/"
    trm_path = "/Volumes/STR-SSD/stealingfire/bcn-mapping/PT_5/SORT/THERMAL/"

    main(rgb_path, trm_path)
