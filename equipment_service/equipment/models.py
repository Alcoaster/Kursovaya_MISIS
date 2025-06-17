from django.db import models


class MaintenanceType(models.Model):
    id = models.SmallIntegerField(db_column='ID_вида_обслуживания', primary_key=True)
    name = models.CharField(db_column='Наименование_обслуживания', unique=True, max_length=30)

    class Meta:
        db_table = 'Вид_обслуживания'


class MaintenanceRegulation(models.Model):
    id = models.BigIntegerField(db_column='ID_норматива', primary_key=True)
    title = models.CharField(db_column='Название_норматива', unique=True, max_length=30)

    class Meta:
        db_table = 'Норматив_обслуживания'


class EquipmentType(models.Model):
    id = models.SmallIntegerField(db_column='ID_типа_оборудования', primary_key=True)
    name = models.CharField(db_column='Наименование_оборудования', max_length=30, unique=True)
    regulation_id = models.ForeignKey(MaintenanceRegulation, models.DO_NOTHING, db_column='ID_норматива', blank=True,
                                      null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Тип_оборудования'


class Equipment(models.Model):
    inventory_number = models.BigIntegerField(db_column='Инвентарный_номер', primary_key=True)
    commissioning_date = models.DateField(db_column='Дата_ввода')
    name = models.CharField(db_column='Наименование_оборудования', max_length=30)
    equipment_type = models.ForeignKey(EquipmentType, models.DO_NOTHING, db_column='ID_типа_оборудования', blank=True,
                                       null=True)

    class Meta:
        db_table = 'Оборудование'


class MaintenancePeriod(models.Model):
    regulation = models.ForeignKey(MaintenanceRegulation, models.DO_NOTHING, db_column='ID_норматива')
    maintenance_type = models.ForeignKey(MaintenanceType, models.DO_NOTHING, db_column='ID_вида_обслуживания')
    period_months = models.BigIntegerField(db_column='Периодичность')

    class Meta:
        db_table = 'Периодичность работы'
        unique_together = (('regulation', 'maintenance_type'),)


class MaintenancePlan(models.Model):
    scheduled_date = models.DateField(db_column='Плановая_дата')
    status = models.CharField(db_column='Статус', max_length=30)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='Инвентарный_номер')
    maintenance_type = models.ForeignKey(MaintenanceType, models.DO_NOTHING, db_column='ID_вида_обслуживания')

    class Meta:
        db_table = 'План_обслуживания'
        unique_together = (('scheduled_date', 'equipment', 'maintenance_type'),)


class Role(models.Model):
    id = models.BigIntegerField(db_column='ID_роли', primary_key=True)
    name = models.CharField(db_column='Наименование_роли', max_length=30)

    class Meta:
        db_table = 'Роль'


class User(models.Model):
    login = models.CharField(db_column='Логин', primary_key=True, max_length=30)
    password = models.CharField(db_column='Пароль', max_length=30)
    first_name = models.CharField(db_column='Имя', max_length=30)
    last_name = models.CharField(db_column='Фамилия', max_length=30)
    middle_name = models.CharField(db_column='Отчество', max_length=30, blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, db_column='ID_роли', blank=True, null=True)

    class Meta:
        db_table = 'Пользователь'
