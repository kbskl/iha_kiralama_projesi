from enum import Enum

"""
Açıklama:
Uygulama içinde kullanılacak sabitler bu dosyada bir enum altında toplanmıştır.
Bunun sebebi forms veya modellerde kullanırken tuple oluşturma işlemini kolaylaştırmak ve rahatça kontrol etmek.
"""


class GeneralEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class GenderEnum(GeneralEnum):
    male = 'Erkek'
    female = 'Kadın'


class StatusTypeEnum(GeneralEnum):
    active = 'Aktif'
    passive = 'Pasif'
