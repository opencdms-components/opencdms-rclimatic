from io import BytesIO
import logging
import os
import PIL.Image as Image
from rpy2.robjects import r, default_converter, conversion, globalenv
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def windrose(obs):
    rpy2_logger.setLevel(logging.ERROR)

    script = os.path.join(
        os.path.dirname(__file__),
        'windrose.r',
    )

    r.source(script)

    with localconverter(default_converter + pandas2ri.converter):
        _obs = conversion.py2rpy(obs)

    globalenv['observations'] = _obs

    r(f"""
library('magick')
figure <- image_graph(width = 350, height = 350, res = 96)
data=observations
ob_time=as.POSIXct(data$ob_time,tz='UTC')
data=cbind(ob_time, data[,3:4])

windrose(data,'838','Bracknell Beaufort Park')

image <- image_write(figure, path = NULL, format = "png")
    """)
    image_data = globalenv['image']
    image = Image.open(BytesIO(bytes(image_data)))

    return image
