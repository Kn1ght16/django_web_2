# django_web_2
Product:

name (CharField) - наименование продукта
description (TextField) - описание продукта
image (ImageField) - изображение продукта (превью)
category (ForeignKey) - категория продукта
price (DecimalField) - цена за покупку
created_at (DateTimeField) - дата создания продукта
updated_at (DateTimeField) - дата последнего изменения продукта
Category:

name (CharField) - наименование категории
description (TextField) - описание категории