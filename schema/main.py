from schema import Schema, Forbidden, SchemaError, Use, And, Optional, Hook, SchemaForbiddenKeyError, SchemaWrongKeyError
import pprint

pp = pprint.PrettyPrinter().pprint

    # id = Column(Integer, primary_key=True)
    # account_status = Column(Account_status, default=cfg.DEFAULT_USER_STATUS,
    #                         nullable=False)
    # confirmation_link = Column(String, nullable=False)
    # cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
    #                    unique=True, nullable=False)

    # email = Column(String, unique=True, nullable=False)
    # name = Column(String, nullable=False)
    # surname = Column(String, nullable=False)
    # password = Column(TEXT, nullable=False)
    # service_status = Column(Service_status, default='user', nullable=False)
    # # secondary info
    # phone = Column(String, nullable=True)
    # organization = Column(String, nullable=True)
    # position = Column(String, nullable=True)
    # country = Column(String, nullable=True)
    # bio = Column(TEXT, nullable=True)

# def customForbidden(key, scope, error):
#     pp('{} {} {}'.format(key, scope, error))

class customForbidden(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(customForbidden, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError('Forbidden key encountered: {} in {}'.format(nkey, data), self._error)

class unknownKey(Hook):
    def __init__(self, *args, **kwargs):
        kwargs["handler"] = self._default_function
        super(unknownKey, self).__init__(*args, **kwargs)

    def _default_function(self, nkey, data, error):
        raise SchemaForbiddenKeyError('Forbidden key encountered: {} in {}'.format(nkey, data), '{}: {}'.format(self._error, nkey))

schema = Schema(
        {
            customForbidden('id', error='Cannot change id!'): object,
            customForbidden('account_status', error='Cannot change account status!'): object,
            customForbidden('confirmation_link', error='Cannot change confirmation link!'): object,
            customForbidden('cookie_id', error='Cannot change cookie_id!'): object,
            Optional('email'): And(str, error='Email is not a string!'),
            Optional('name'): And(str, error='Name is not a string!'),
            Optional('surname'): And(str, error='Surname is not a string!'),
            customForbidden('password', error='Cannot change password through here!'): object,
            customForbidden('service_status', error='Cannot change service_status!'): object,
            Optional('phone'): And(str, error='Phone is not a string!'),
            Optional('organization'): And(str, error='Organisation is not a string!'),
            Optional('position'): And(str, error='Position is not a string!'),
            Optional('country'): And(str, error='Country is not a string!'),
            Optional('bio'): And(str, error='Bio is not a string!'),
            unknownKey(str, error='Unknown key detected!'): object
        }#, Расскомментировать эти строчки и заккоментровать строчку с unknownKey для игнорирования лишних ключей
        #ignore_extra_keys=True
)

data = [
    {

    },
    {
        'id': '1234',
    },
    {
        'id': 1234,
    },
    {
        'account_status': 'active'
    },
    {
        'confirmation_link': '123456'
    },
    {
        'cookie_id': '1234'
    },
    {
        'email': 'mail@mail.mail'
    },
    {
        'email': 1234
    },
    {
        'name': 1234
    },
    {
        'name': []
    },
    {
        'name': 'Test',
    },
    {
        'some_key': 'asdf'
    },
    {
        'email': 'mail@mail.mail',
        'name': 'Huilo',
        'surname': 'Huilovsky',
        'phone': '1234567',
        'organization': 'HSE',
        'position': 'Huilo',
        'country': 'Ru',
        'bio': 'Hui s gory'
    }
]

for i in data:
    try:
        pp(i)
        valid = schema.validate(i)
        if valid != {}:
            print('Valid!')

    except SchemaForbiddenKeyError as e:
        pp(e)
        for err in e.errors:
            print('\tError: {}'.format(err))
        for err in e.autos:
            print('\tAutos: {}'.format(err))
    except SchemaWrongKeyError as e:
        pp(e)
        for err in e.errors:
            print('\tError: {}'.format(err))
        for err in e.autos:
            print('\tAutos: {}'.format(err))
    except SchemaError as e:
        pp(e)
        for err in e.errors:
            print('\tError: {}'.format(err))
        for err in e.autos:
            print('\tAutos: {}'.format(err))
    except Exception as e:
        pp(e)
    finally:
        print()



