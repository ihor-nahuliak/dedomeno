from multiselectfield import MultiSelectField

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField


class TerritorialEntity(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    depth = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code_idealista = models.CharField(max_length=50, null=True, blank=True)
    code_idealista_raw = models.CharField(max_length=500, null=True, blank=True)
    name_idealista = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='children', help_text='father')

    def get_all_children_properties(self):
        query_list = [i.property.all() for i in self.get_all_children()]
        query_final = query_list.pop()
        for query in [i.property.all() for i in self.get_all_children()]:
            query_final = query_final | query
        return query_final

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def get_all_parents(self):
        parents = [self]
        if self.parent is not None:
            parent = self.parent
            parents.extend(parent.get_all_parents())
        return parents

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("A user cannot have itself or one of its' children as parent.")

    '''
    def get_childrens(self, also_self=True):
        i.children.all() for i in madrid.children.all()
            """ return a family tree for a Person object """

            children = self.children.all()

            if not children:
                # this person has no children, recursion ends here
                return {'name': person.name, 'children': []}

            # this person has children, get every child's family tree
            return {
                'name': person.name,
                'children': [get_family_tree(child) for child in children],
            }

    def get_path(self):
        go = True
        reverse_path = [self]
        parent = self.parent
        while go:
            if parent:
                reverse_path.append(parent)
                parent = parent.parent
            else:
                go = False
        return reverse_path[::-1]

    def get_ascendent(self, depth):
        if depth < self.depth:
            pass
        else:
            return None
    '''
    def __str__(self):
        return '{%s} depth=%i' % (self.code_idealista, self.depth)


class RealEstate(models.Model):
    """
    Stores a Real Estate entity.
    """
    name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True)
    logo = models.URLField(null=True, blank=True)
    web = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    html = models.TextField(blank=True, null=True)
    desc = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    geocode = models.ManyToManyField(TerritorialEntity)

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    Father Model for all the properties; if :model:`houses.RealEstate`
    is blank there is not a real estate involved
    """
    # main data
    title = models.CharField(max_length=500, null=True)
    url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    html = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    TRANSACTION_CHOICES = (
        ('rent', 'rent'),
        ('sale', 'sale'),
    )
    transaction = models.CharField(choices=TRANSACTION_CHOICES, null=True, blank=True, max_length=4)
    PROPERTY_CHOICES = (
        ('house', 'house'),
        ('room', 'room'),
        ('office', 'office'),
        ('garage', 'garage'),
        ('land', 'land'),
        ('commercial', 'commercial'),
        ('storeroom', 'storeroom'),
        ('building', 'building'),
    )
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=200, blank=True, null=True)
    # https://docs.djangoproject.com/en/1.8/ref/contrib/postgres/fields/#arrayfield
    # equipment = ArrayField(models.CharField(max_length=5000, blank=True, null=True), null=True)
    # contact
    name = models.CharField(blank=True, max_length=500, null=True)
    phone_1 = models.CharField(blank=True, max_length=30, null=True)
    phone_2 = models.CharField(blank=True, max_length=30, null=True)
    real_estate = models.ForeignKey(RealEstate, blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name='property',
                                    help_text='If blank there is not a real estate involved')
    real_estate_raw = models.CharField(blank=True, max_length=200, null=True)
    price_raw = models.IntegerField(blank=True, null=True)
    geocode_raw = ArrayField(models.CharField(max_length=200, blank=True, null=True), default=[])
    geocode = models.ForeignKey(TerritorialEntity, blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='property')
    address_path = ArrayField(models.CharField(max_length=200, blank=True, null=True), default=[])
    address_province = models.CharField(max_length=200, blank=True, null=True)
    address_raw = models.CharField(max_length=2000, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    address_exact = models.NullBooleanField()
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    date_raw = models.DateField(blank=True, null=True)
    online = models.NullBooleanField(default=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class Price(models.Model):
    """
    Stores the price of a :model:`houses.Property` for a period of time.
    """
    value = models.IntegerField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    property_price = models.ForeignKey(Property, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '[' + str(self.date_start) + ']-[' + str(self.date_end) + ']: ' + str(self.value)


class Date(models.Model):
    """
    Stores the period of time a :model:`houses.Property` has been online
    """
    online = models.DateField(blank=True, null=True)
    offline = models.DateField(blank=True, null=True)
    property_date = models.ForeignKey(Property, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '[' + str(self.online) + ']-[' + str(self.offline) + ']'


class House(Property):
    """
    Stores a House type :model:`houses.Property`
    """
    # house data
    house_type = models.CharField(max_length=200, null=True, blank=True)
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True, default=0)
    wc = models.IntegerField(blank=True, null=True, default=0)
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    outside = models.CharField(max_length=20, null=True, blank=True)
    ORIENTATION_CHOICES = (
        ('norte', 'norte'),
        ('noreste', 'noreste'),
        ('este', 'este'),
        ('sureste', 'sureste'),
        ('sur', 'sur'),
        ('suroeste', 'suroeste'),
        ('oeste', 'oeste'),
        ('noroeste', 'noroeste'),
    )
    orientation = MultiSelectField(choices=ORIENTATION_CHOICES, null=True, blank=True, max_length=30, max_choices=8)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    construction_year = models.IntegerField(blank=True, null=True)
    # equipment
    has_garage = models.NullBooleanField()
    terrace = models.NullBooleanField()
    elevator = models.NullBooleanField()
    chimney = models.NullBooleanField()
    swimming_pool = models.NullBooleanField()
    air_conditioning = models.NullBooleanField()
    store_room = models.NullBooleanField()
    builtin_wardrobes = models.NullBooleanField()
    furnished = models.NullBooleanField()
    furnished_kitchen = models.NullBooleanField()
    garden = models.NullBooleanField()


class Room(Property):
    """
    Stores a Room type :model:`houses.Property`
    """
    # Características básicas
    house_type = models.CharField(max_length=200, null=True, blank=True)
    m2_total = models.IntegerField(blank=True, null=True)
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    elevator = models.NullBooleanField()
    wc = models.IntegerField(blank=True, null=True)
    min_month_stay = models.IntegerField(blank=True, null=True)
    people_max = models.IntegerField(blank=True, null=True)
    people_now_living_gender = models.CharField(max_length=200, null=True, blank=True)
    people_now_living_age_min = models.IntegerField(blank=True, null=True)
    people_now_living_age_max = models.IntegerField(blank=True, null=True)
    smoking_allowed = models.NullBooleanField()
    pet_allowed = models.NullBooleanField()
    # Looking for
    looking_for_male = models.NullBooleanField()
    looking_for_female = models.NullBooleanField()
    looking_for_student = models.NullBooleanField()
    looking_for_worker = models.NullBooleanField()
    gay_friendly = models.NullBooleanField()
    # Equipment
    air_conditioning = models.NullBooleanField()
    internet = models.NullBooleanField()
    builtin_wardrobes = models.NullBooleanField()
    furnished = models.NullBooleanField()
    house_cleaners = models.NullBooleanField()


class Office(Property):
    """
    Stores a Office type :model:`houses.Property`
    """
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    num_of_floors = models.IntegerField(blank=True, null=True)
    distribution = models.CharField(max_length=200, null=True, blank=True)
    kitchen = models.NullBooleanField()
    wc = models.IntegerField(blank=True, null=True)
    wc_location = models.CharField(max_length=200, null=True, blank=True)
    ORIENTATION_CHOICES = (
        ('norte', 'norte'),
        ('noreste', 'noreste'),
        ('este', 'este'),
        ('sureste', 'sureste'),
        ('sur', 'sur'),
        ('suroeste', 'suroeste'),
        ('oeste', 'oeste'),
        ('noroeste', 'noroeste'),
    )
    orientation = MultiSelectField(choices=ORIENTATION_CHOICES, null=True, blank=True, max_length=30, max_choices=8)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    has_garage = models.NullBooleanField()
    # Building
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    outside = models.CharField(max_length=20, null=True, blank=True)
    elevators = models.IntegerField(blank=True, null=True)
    office_type = models.CharField(max_length=20, null=True, blank=True)
    janitor = models.NullBooleanField()
    access_control = models.NullBooleanField()
    security_system = models.NullBooleanField()
    security_door = models.NullBooleanField()
    fire_extinguishers = models.NullBooleanField()
    fire_detectors = models.NullBooleanField()
    sprinklers = models.NullBooleanField()
    fire_door = models.NullBooleanField()
    emergency_exit = models.NullBooleanField()
    emergency_exit_lights = models.NullBooleanField()
    # Equipment
    store_room = models.NullBooleanField()
    hot_water = models.NullBooleanField()
    heating = models.NullBooleanField()
    air_conditioning_cold = models.NullBooleanField()
    air_conditioning_hot = models.NullBooleanField()
    double_glazed_windows = models.NullBooleanField()
    false_ceiling = models.NullBooleanField()
    false_floor = models.NullBooleanField()


class Garage(Property):
    """
    Stores a Garage type :model:`houses.Property`
    """
    # Basic
    garage_type = models.CharField(max_length=200, null=True, blank=True)
    garage_number = models.IntegerField(blank=True, null=True)
    covered = models.NullBooleanField()
    elevator = models.NullBooleanField()
    # Equipment
    automatic_door = models.NullBooleanField()
    security_cameras = models.NullBooleanField()
    alarm = models.NullBooleanField()
    security_guard = models.NullBooleanField()


class Land(Property):
    """
    Stores a Land type :model:`houses.Property`
    """
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m2_min_rent = models.IntegerField(blank=True, null=True)
    m2_min_sale = models.IntegerField(blank=True, null=True)
    m2_to_build = models.IntegerField(blank=True, null=True)
    access = models.CharField(max_length=200, null=True, blank=True)
    nearest_town = models.CharField(max_length=200, null=True, blank=True)
    # Urban situation
    ground = models.CharField(max_length=200, null=True, blank=True)
    zoned = models.CharField(max_length=200, null=True, blank=True)
    building_floors = models.IntegerField(blank=True, null=True)
    # Equipment
    sewerage = models.NullBooleanField()
    street_lighting = models.NullBooleanField()
    water = models.NullBooleanField()
    electricity = models.NullBooleanField()
    sidewalks = models.NullBooleanField()
    natural_gas = models.NullBooleanField()


class Commercial(Property):
    """
    Stores a Commercial type :model:`houses.Property`
    """
    # Basic
    commercial_type = models.CharField(max_length=200, null=True, blank=True)
    transfer_price = models.IntegerField(blank=True, null=True)
    m2_total = models.IntegerField(blank=True, null=True)
    m2_to_use = models.IntegerField(blank=True, null=True)
    m2_terrain = models.IntegerField(blank=True, null=True)
    num_of_floors = models.IntegerField(blank=True, null=True)
    distribution = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    corner = models.NullBooleanField()
    show_windows = models.IntegerField(blank=True, null=True)
    last_activity = models.CharField(max_length=200, null=True, blank=True)
    preservation = models.CharField(max_length=100, null=True, blank=True)
    wc = models.IntegerField(blank=True, null=True)
    # Building
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    facade = models.CharField(max_length=200, null=True, blank=True)
    # Equipment
    air_conditioning = models.NullBooleanField()
    alarm_system = models.NullBooleanField()
    store_room = models.NullBooleanField()
    heating = models.NullBooleanField()
    kitchen = models.NullBooleanField()
    security_door = models.NullBooleanField()
    smoke_extractor = models.NullBooleanField()


class StoreRoom(Property):
    """
    Stores a StoreRoom type :model:`houses.Property`
    """
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m_height = models.IntegerField(blank=True, null=True)
    access_24h = models.NullBooleanField()
    limited_parking = models.NullBooleanField()


class Building(Property):
    """
    Stores a Building type :model:`houses.Property`
    """
    # Basic
    m2_total = models.IntegerField(blank=True, null=True)
    m2_min_rent = models.IntegerField(blank=True, null=True)
    building_type = models.CharField(max_length=200, null=True, blank=True)
    elevator_num = models.IntegerField(blank=True, null=True)
    floor_num = models.CharField(max_length=200, null=True, blank=True)
    garage_num = models.CharField(max_length=200, null=True, blank=True)
    security = models.NullBooleanField()
    preservation = models.CharField(max_length=100, null=True, blank=True)
    tenant = models.CharField(max_length=200, null=True, blank=True)
    house_num = models.IntegerField(blank=True, null=True)
    construction_year = models.IntegerField(blank=True, null=True)
