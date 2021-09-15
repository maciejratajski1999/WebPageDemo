import os
from app.models import *

def on_init_utils(app):
    app = app

    def delete_unused_images():
        static, thumbnails, pictures = 'static', 'thumbnails', 'pictures'
        pictures_path = os.path.join(app.root_path, static, pictures)
        pictures = list(os.listdir(pictures_path))
        pictures = [os.path.join(pictures_path, picture) for picture in pictures]
        thumbnails_path = os.path.join(app.root_path, static, thumbnails)
        thumbnails = list(os.listdir(thumbnails_path))
        thumbnails = [os.path.join(thumbnails_path, thumbnail) for thumbnail in thumbnails]
        static_files = pictures + thumbnails
        static_files = [file for file in static_files if os.path.splitext(file)[1] == '.png']
        pictures = [picture.path for picture in Picture.query.all()]
        thumbnails = [thumbnail.path for thumbnail in Thumbnail.query.all()]
        post_pictures = [post_picture.path for post_picture in PostPicture.query.all()]
        for filename in static_files:
            subpath, file = os.path.split(filename)
            image_path = os.path.join(os.path.split(subpath)[1], file)
            if image_path not in pictures + thumbnails + post_pictures:
                print(f"deleting unused file: {filename}")
                os.remove(filename)


    def save_images():
        new_images = []
        all_models = [picture for picture in Picture.query.all()] + [
            thumbnail for thumbnail in Thumbnail.query.all()] + [
                         post_picture for post_picture in PostPicture.query.all()]
        to_save = [model for model in all_models if model.image_id == None]
        for model in to_save:
            path = os.path.join(f'app/static/{model.path}')
            file_binary = convert_img_to_binary(path)
            image = add_image(file_binary)
            model.image_id = image.id
            new_images.append(image)
        db.session.commit()
        return new_images


    def generate_from_image(image, child):
        path = os.path.join(app.root_path, f'static/{child.path}')
        with open(path, 'wb') as new_image:
            img_byte_code = decode_binary_to_img(image.file)
            new_image.write(img_byte_code)


    def generate_static_pngs():
        static_files = list(os.listdir('app/static/pictures')) + list(os.listdir('app/static/thumbnails'))
        static_files = [file for file in static_files if os.path.splitext(file)[1] == '.png']
        images = Image.query.all()
        for image in images:
            children = image.get_children()
            for child in children:
                if os.path.basename(child.path) not in static_files:
                    generate_from_image(image, child)
                else:
                    continue

    def delete_all_images():
        for image in Image.query.all():
            image.delete()

    return delete_unused_images, save_images, generate_static_pngs, delete_all_images