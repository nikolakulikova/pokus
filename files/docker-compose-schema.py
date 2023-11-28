{
    'version': {
        'required': True,
        'type': 'string'
    },
    'volumes': {
        'required': True,
        'type': 'dict',
        'schema': {
             'postgres_data': {
                 'required': True,
                 'type': 'dict',
                 'driver': {
                         'required': True,
                         'type': 'string',
                    }
            }
        }
    },
    'networks': {
        'required': True,
        'type': 'dict',
        'schema': {
             'postgres-network': {
                 'required': True,
                 'type': 'dict',
                 'driver': {
                         'required': True,
                         'type': 'string',
                    }
            }
        }
    },
    'services': {
        'required': True,
        'type': 'dict',
        'schema': {
             'db': {
                 'required': True,
                 'type': 'dict',
                 'container_name': {
                         'required': True,
                         'type': 'string',
                    },
                 'image': {
                         'required': True,
                         'type': 'string',
                    },
                 'volumes': {
                         'required': True,
                         'type': 'string',
                    },
                 'ports': {
                         'required': True,
                         'type': 'string',
                    },
                 'networks': {
                         'required': True,
                         'type': 'string',
                    },
                 'environment': {
                         'required': True,
                         'type': 'dict',
                         'schema': {
                             'POSTGRES_DB': {
                                 'required': True,
                                 'type': 'string',
                             },
                             'POSTGRES_USER': {
                                 'required': True,
                                 'type': 'string',
                             },
                             'POSTGRES_PASSWORD': {
                                 'required': True,
                                 'type': 'string',
                             },
                         }
                    }
            },
             'django_application': {
                 'required': True,
                 'type': 'dict',
                 'schema': {
                    'container_name': {
                             'required': True,
                             'type': 'string',
                        },
                 'image': {
                         'required': True,
                         'type': 'string',
                    },
                 'volumes': {
                         'required': True,
                         'type': 'string',
                    },
                 'ports': {
                         'required': True,
                         'type': 'string',
                    },
                 'networks': {
                         'required': True,
                         'type': 'string',
                    },
                 'environment': {
                         'required': True,
                         'type': 'dict',
                         'schema': {
                             'POSTGRES_DB': {
                                 'required': True,
                                 'type': 'string',
                             },
                             'POSTGRES_USER': {
                                 'required': True,
                                 'type': 'string',
                             },
                             'POSTGRES_PASSWORD': {
                                 'required': True,
                                 'type': 'string',
                             },
                         }
                 }
            }
             }

        }}
}