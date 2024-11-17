from django.db import models
from django_jsonform.models.fields import JSONField

class Directory(models.Model):
    LABELS_SCHEMA = {
        "type": "array",
        "items": {
            "type": "string"
        },
    }
    directoryName = models.CharField(max_length=200, verbose_name="Название справочника")
    directoryItems = JSONField(schema=LABELS_SCHEMA, null=True, blank=True, verbose_name="Элементы справочника")

    def __str__(self):
        return self.directoryName

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

def dynamic_sections_schema():
    directories = list(Directory.objects.all().values_list('directoryName', flat=True))
    SECTION_SCHEMA = {
        "type": "array",
        "items": {
            "type": "dict",
            "keys": {
                "strFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                },
                "numberFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                }
                            }
                        }
                    }
                },
                "datetimeFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "format": "datetime"
                                }
                            }
                        }
                    }
                },
                "directories": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {
                                "type": "string",
                                "choices": directories,
                            },
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                }
                            }
                        }
                    }
                },
            },
        },
    }
    return SECTION_SCHEMA

def dynamic_no_sections_schema():
    directories = list(Directory.objects.all().values_list('directoryName', flat=True))
    SECTION_SCHEMA = {
        "type": "dict",
        "keys": {
                "strFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                },
                "numberFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                }
                            }
                        }
                    }
                },
                "datetimeFields": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "format": "datetime"
                                }
                            }
                        }
                    }
                },
                "directories": {
                    "type": "array",
                    "items": {
                        "type": "dict",
                        "keys": {
                            "name": {
                                "type": "string",
                                "choices": directories,
                            },
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                }
                            }
                        }
                    }
                },
            },
        }
    return SECTION_SCHEMA

def dynamic_property_sections_schema():
    properties = list(Sections.objects.all().values_list('propertyName', flat=True))
    directories = list(Directory.objects.all().values_list('directoryName', flat=True))
    res = properties.extend(directories)
    SECTIONS_SCHEMA = {
        "type": "array",
        "items": {
            "type": "dict",
            "keys": {
                "property": {
                    "type": "string",
                    "choices": res
                },
                "sections": {
                    "type": "dict",
                    "keys": {
                        "name": {
                            "type": "string"
                        },
                        "values": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                },
                "value": {
                    "type": "string",
                    "readonly": True
                }
            }
        }
    }
    return SECTIONS_SCHEMA


class Sections(models.Model):
        VALUE_SCHEMA = {
            "type": "array",
            "items": {
                "type": "dict",
                "keys": {
                    "strFields": {
                            "type": "array",
                            "items": {
                                "type": "string",
                            }
                    },
                    "numberFields": {
                        "type": "array",
                        "items": {
                            "type": "number",
                        }
                    },
                    "datetimeFields": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "format": "datetime"
                        }
                    },
                },
            },
        }
        propertyName = models.CharField(max_length=200, verbose_name="Название свойства")
        sections = JSONField(schema=dynamic_sections_schema, null=True, blank=True, verbose_name="Разрезы")
        values = JSONField(schema=VALUE_SCHEMA, null=True, blank=True, verbose_name="Значения")

        def __str__(self):
            return "Разрезы " + self.propertyName

        class Meta:
            verbose_name = 'Разрез'
            verbose_name_plural = 'Разрезы'


class InsuranceProduct(models.Model):
    productName = models.CharField(max_length=200, verbose_name="Название продукта")
    properties = JSONField(schema=dynamic_no_sections_schema, null=True, blank=True, verbose_name="Свойства")
    propertiesSections = JSONField(schema=dynamic_property_sections_schema, null=True, blank=True, verbose_name="Свойства с разрезами")

    def __str__(self):
        return self.productName

    def save(self, *args, **kwargs):
        propertiesSections = self.propertiesSections
        sections = Sections.objects.all()
        #for i in range(len(propertiesSections)):
        print(self.propertiesSections)
        print(list(sections))
        super(InsuranceProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Страховой продукт'
        verbose_name_plural = 'Страховые продукты'
