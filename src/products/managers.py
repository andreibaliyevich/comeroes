from django.db import models


class ProductManager(models.Manager):
    """ Product Manager """

    def search(self, query=None):
        qs = self.get_queryset()

        if query:
            query = query.lower()
            id_list = []

            for obj in qs:
                if query in obj.name.lower():
                    id_list.append(obj.id)
                else:
                    for obj_trans in obj.translations.all():
                        if query in obj_trans.name.lower():
                            id_list.append(obj.id)
                            break

            qs = qs.filter(id__in=id_list)

        return qs
