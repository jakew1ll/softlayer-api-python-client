"""
usage: sl image [<command>] [<args>...] [options]

Manage compute images

The available commands are:
  delete  Delete an image
  detail  Output details about an image
  list    List images
"""
# :license: MIT, see LICENSE for more details.

from SoftLayer import ImageManager

from SoftLayer.CLI import CLIRunnable, Table, KeyValueTable, blank, resolve_id


class ListImages(CLIRunnable):
    """
usage: sl image list [--public | --private] [options]

List images

Options:
  --private  Display only private images
  --public   Display only public images
"""
    action = 'list'

    def execute(self, args):
        image_mgr = ImageManager(self.client)

        neither = not any([args['--private'], args['--public']])
        mask = 'id,accountId,name,globalIdentifier,blockDevices,parentId'

        images = []
        if args['--private'] or neither:
            for image in image_mgr.list_private_images(mask=mask):
                image['visibility'] = 'private'
                images.append(image)

        if args['--public'] or neither:
            for image in image_mgr.list_public_images(mask=mask):
                image['visibility'] = 'public'
                images.append(image)

        t = Table(['id', 'account', 'visibility', 'name', 'global_identifier'])

        images = filter(lambda x: x['parentId'] == '', images)
        for image in images:
            t.add_row([
                image['id'],
                image.get('accountId', blank()),
                image['visibility'],
                image['name'].strip(),
                image.get('globalIdentifier', blank()),
            ])

        return t


class DetailImage(CLIRunnable):
    """
usage: sl image detail <identifier> [options]

Get details for an image
"""
    action = 'detail'

    def execute(self, args):
        image_mgr = ImageManager(self.client)
        image_id = resolve_id(image_mgr.resolve_ids,
                              args.get('<identifier>'),
                              'image')

        image = image_mgr.get_image(image_id)

        t = KeyValueTable(['Name', 'Value'])
        t.align['Name'] = 'r'
        t.align['Value'] = 'l'

        t.add_row(['id', image['id']])
        t.add_row(['account', image.get('accountId', blank())])
        t.add_row(['name', image['name'].strip()])
        t.add_row(['global_identifier',
                   image.get('globalIdentifier', blank())])

        return t


class DeleteImage(CLIRunnable):
    """
usage: sl image delete <identifier> [options]

Get details for an image
"""
    action = 'delete'

    def execute(self, args):
        image_mgr = ImageManager(self.client)
        image_id = resolve_id(image_mgr.resolve_ids,
                              args.get('<identifier>'),
                              'image')

        image_mgr.delete_image(image_id)
