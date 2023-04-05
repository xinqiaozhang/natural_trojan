

import wand.image
import wand.color
import wand.drawing
import math
def Gotham_filter(image: wand.image.Image):
    """
    modified from https://github.com/acoomans/instagram-filters/blob/master/instagram_filters/filters/gotham.py
    :param image: provided image
    :return: new filtered image
    """
    filtered_image = image.clone()
    filtered_image.modulate(120, 10, 100)
    filtered_image.colorize(wand.color.Color('#222b6d'), wand.color.Color('#333333'))
    filtered_image.gamma(.9)
    filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
    filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
    return filtered_image

def Nashville_filter(image: wand.image.Image):
        """
        modified from https://github.com/acoomans/instagram-filters/blob/master/instagram_filters/filters/nashville.py
        :param image:
        :return: new filtered image
        """
        filtered_image = image.clone()
        # self._colortone(filtered_image, '#222b6d', 50, True)
        dst_percent = 50
        mask_src = filtered_image.clone()
        mask_src.colorspace = 'gray'
        # if invert:
        mask_src.negate()
        mask_src.alpha_channel = 'copy'

        src = filtered_image.clone()
        src.colorize(wand.color.Color('#222b6d'), wand.color.Color('#FFFFFF'))
        src.composite_channel('alpha', mask_src, 'copy_alpha')

        filtered_image.composite_channel('default_channels', src, 'blend',
                                arguments=str(dst_percent) + "," + str(100 - dst_percent))

        # self._colortone(filtered_image, '#f7daae', 50, False)
        mask_src = filtered_image.clone()
        mask_src.colorspace = 'gray'
        mask_src.alpha_channel = 'copy'

        src = filtered_image.clone()
        src.colorize(wand.color.Color('#f7daae'), wand.color.Color('#FFFFFF'))
        src.composite_channel('alpha', mask_src, 'copy_alpha')
        filtered_image.composite_channel('default_channels', src, 'blend',
                                arguments=str(dst_percent) + "," + str(100 - dst_percent))

        # self._colortone(filtered_image, '#222b6d', 50, True)
        # self._colortone(filtered_image, '#f7daae', 50, False)
        # filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
        # filtered_image.modulate(100, 150, 100)
        # filtered_image.auto_gamma()

        filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
        filtered_image.modulate(100, 150, 100)
        filtered_image.auto_gamma()
        return filtered_image

def Kelvin_filter(image: wand.image.Image):
        """
        modified from https://github.com/acoomans/instagram-filters/blob/master/instagram_filters/filters/kelvin.py
        :param image: provided image
        :return: new filtered image
        """
        filtered_image = image.clone()
        filtered_image.auto_gamma()
        filtered_image.modulate(120, 50, 100)
        with wand.drawing.Drawing() as draw:
            draw.fill_color = '#FF9900'
            draw.fill_opacity = 0.2
            draw.rectangle(left=0, top=0, width=filtered_image.width, height=filtered_image.height)
            draw(filtered_image)
        return filtered_image

def Lomo_filter(image: wand.image.Image):
        """
        modified from https://github.com/acoomans/instagram-filters/blob/master/instagram_filters/filters/lomo.py
        :param image: provided image
        :return: new filtered image
        """
        filtered_image = image.clone()
        filtered_image.level(.5, channel="R")
        filtered_image.level(.5, channel="G")
        # self._vignette(filtered_image)
        color_1 = 'none'
        color_2 = 'black'
        crop_factor = 1.5
        crop_x = math.floor(filtered_image.width * crop_factor)
        crop_y = math.floor(filtered_image.height * crop_factor)
        src = filtered_image.clone()
        # pdb.set_trace()
        # src = filtered_image
        src.pseudo(width=crop_x, height=crop_y, pseudo='radial-gradient:' + color_1 + '-' + color_2)
        src.crop(0, 0, width=filtered_image.width, height=filtered_image.height, gravity='center')
        src.reset_coords()
        filtered_image.composite_channel('default_channels', src, 'multiply')
        filtered_image.merge_layers('flatten')


        return filtered_image

def Toaster_filter(image: wand.image.Image) :
        """
        modified from https://github.com/acoomans/instagram-filters/blob/master/instagram_filters/filters/toaster.py
        :param image: provided image
        :return: new filtered image
        """

        filtered_image = image.clone()
        # self._colortone(filtered_image, '#330000', 50, True)
        dst_percent = 50
        mask_src = filtered_image.clone()
        mask_src.colorspace = 'gray'
        # if invert:
        mask_src.negate()
        mask_src.alpha_channel = 'copy'

        src = filtered_image.clone()
        src.colorize(wand.color.Color('#330000'), wand.color.Color('#FFFFFF'))
        src.composite_channel('alpha', mask_src, 'copy_alpha')

        filtered_image.composite_channel('default_channels', src, 'blend',
                                arguments=str(dst_percent) + "," + str(100 - dst_percent))


        filtered_image.modulate(150, 80, 100)
        filtered_image.gamma(1.2)
        filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
        filtered_image.sigmoidal_contrast(True, 3, .5 * filtered_image.quantum_range)
        # self._vignette(filtered_image, 'none', 'LavenderBlush3')
        color_1 = 'none'
        # color_2 = 'black'
        crop_factor = 1.5
        color_2 = 'LavenderBlush3'

        crop_x = math.floor(filtered_image.width * crop_factor)
        crop_y = math.floor(filtered_image.height * crop_factor)
        src = filtered_image.clone()
        src.pseudo(width=crop_x, height=crop_y, pseudo='radial-gradient:' + color_1 + '-' + color_2)
        src.crop(0, 0, width=filtered_image.width, height=filtered_image.height, gravity='center')
        src.reset_coords()
        filtered_image.composite_channel('default_channels', src, 'multiply')
        filtered_image.merge_layers('flatten')

        # self._vignette(filtered_image, '#ff9966', 'none')
        color_1 = '#ff9966'
        color_2 = 'none'
        crop_factor = 1.5
        # color_1 = '#ff9966'

        crop_x = math.floor(filtered_image.width * crop_factor)
        crop_y = math.floor(filtered_image.height * crop_factor)
        # src = filtered_image.Image()
        src = filtered_image.clone()

        src.pseudo(width=crop_x, height=crop_y, pseudo='radial-gradient:' + color_1 + '-' + color_2)
        src.crop(0, 0, width=filtered_image.width, height=filtered_image.height, gravity='center')
        src.reset_coords()
        filtered_image.composite_channel('default_channels', src, 'multiply')
        filtered_image.merge_layers('flatten')
        return filtered_image

