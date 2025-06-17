from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Equipment, MaintenancePlan, MaintenanceType, EquipmentType, MaintenanceRegulation

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Equipment, MaintenancePlan, MaintenanceType, EquipmentType, MaintenanceRegulation


def add_equipment(request):
    if request.method == 'POST':
        try:
            Equipment.objects.create(
                inventory_number=request.POST.get('inventory_number'),
                name=request.POST.get('name'),
                equipment_type_id=request.POST.get('equipment_type'),
                commissioning_date=request.POST.get('commissioning_date')
            )
            messages.success(request, 'Оборудование успешно добавлено!')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении оборудования: {e}')

        return redirect('equipment')

    return redirect('equipment')


def equipment_view(request):
    today = timezone.now().date()

    equipment_list = []

    for eq in Equipment.objects.all():
        # Все ремонты по этому оборудованию
        maintenance_qs = MaintenancePlan.objects.filter(equipment=eq).order_by('scheduled_date')

        # Последний ремонт — который был до сегодняшней даты
        last_maintenance = maintenance_qs.filter(scheduled_date__lt=today).last()

        # Следующий ремонт — который запланирован на сегодня или позже
        next_maintenance = maintenance_qs.filter(scheduled_date__gte=today).first()

        # Статус можно взять от последнего ремонта
        status = 'Исправен'

        equipment_list.append({
            'name': eq.name,
            'status': status,
            'last_maintenance': last_maintenance.scheduled_date if last_maintenance else 'нет',
            'next_maintenance': next_maintenance.scheduled_date if next_maintenance else 'нет',
            'equipment_type': eq.equipment_type.name if eq.equipment_type else 'Не указано'
        })

    context = {
        'equipment_list': equipment_list,
        'equipment_types': EquipmentType.objects.select_related('regulation_id').all(),
        'maintenance_regulations': MaintenanceRegulation.objects.all(),
    }
    return render(request, 'equipment.html', context)


def requests_view(request):
    if request.method == 'POST':
        # Обработка создания новой заявки
        equipment_id = request.POST.get('equipment_id')
        maintenance_type_id = request.POST.get('maintenance_type_id')
        scheduled_date = request.POST.get('scheduled_date')

        MaintenancePlan.objects.create(
            equipment_id=equipment_id,
            maintenance_type_id=maintenance_type_id,
            scheduled_date=scheduled_date,
            status='Запланировано'
        )
        return redirect('requests')  # редирект после создания

    plans = MaintenancePlan.objects.select_related('equipment', 'maintenance_type').all().order_by('scheduled_date')

    plan_data = []

    for plan in plans:
        plan_data.append({
            'order_id': plan.id,
            'equipment_name': plan.equipment.name,
            'maintenance_type': plan.maintenance_type.name,
            'scheduled_date': plan.scheduled_date,
            'status': plan.status,
        })
    context = {
        'plans': plan_data,
        'equipment_list': Equipment.objects.all(),
        'maintenance_types': MaintenanceType.objects.all(),
    }
    return render(request, 'orders.html', context)
