// dashboard/web_interface/static/js/control.js
document.addEventListener('DOMContentLoaded', () => {
    // جلب حالة الصمامات
    fetch('/api/valves')
        .then(response =>{
            // التصحيح: معالجة الأخطاء في fetch
            if (!response.ok) throw new Error('فشل جلب البيانات');
            return response.json();
        })
        .catch(error => {
            console.error('خطأ في الاتصال:', error);
            alert('تعذر الاتصال بالخادم');
        })
        .then(valves => {
            const valveList = document.querySelector('.valve-list');
            valveList.innerHTML = '';
            
            valves.forEach(valve => {
                const valveEl = document.createElement('div');
                valveEl.className = 'valve-card';
                valveEl.innerHTML = `
                    <h3>الصمام ${valve.id}</h3>
                    <p>الحالة: <span class="status">${valve.status === 'open' ? 'مفتوح' : 'مغلق'}</span></p>
                    ${valve.status === 'open' ? `<p>الوقت المتبقي: ${valve.duration_left} دقائق</p>` : ''}
                    <div class="actions">
                        <button class="btn-activate" data-valve="${valve.id}">فتح</button>
                        <button class="btn-deactivate" data-valve="${valve.id}">إغلاق</button>
                    </div>
                `;
                
                valveList.appendChild(valveEl);
            });
            
            // إضافة معالجات الأحداث
            document.querySelectorAll('.btn-activate').forEach(btn => {
                btn.addEventListener('click', () => {
                    const valveId = btn.dataset.valve;
                    const duration = prompt('المدة (دقائق):', '15');
                    if (duration) {
                        activateValve(valveId, parseInt(duration));
                    }
                });
            });
            
            document.querySelectorAll('.btn-deactivate').forEach(btn => {
                btn.addEventListener('click', () => {
                    const valveId = btn.dataset.valve;
                    deactivateValve(valveId);
                });
            });
        });
    
    // إدارة الجداول
    document.getElementById('schedule-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const valveId = document.getElementById('valve-select').value;
        const time = document.getElementById('schedule-time').value;
        const duration = document.getElementById('duration').value;
        
        addSchedule(valveId, time, duration);
    });
    
    // جلب الجداول النشطة
    fetch('/api/schedules')
        .then(response => response.json())
        .then(schedules => {
            const schedulesList = document.getElementById('active-schedules');
            schedulesList.innerHTML = '';
            
            schedules.forEach(schedule => {
                const li = document.createElement('li');
                li.textContent = `الصمام ${schedule.valve_id} - ${schedule.time} (${schedule.duration} دقيقة)`;
                schedulesList.appendChild(li);
            });
        });
});

function activateValve(valveId, duration) {
    fetch(`/api/valves/${valveId}/activate?duration=${duration}`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                alert('تم تفعيل الصمام بنجاح');
                location.reload();
            }
        });
}

function deactivateValve(valveId) {
    fetch(`/api/valves/${valveId}/deactivate`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                alert('تم إيقاف الصمام بنجاح');
                location.reload();
            }
        });
}

function addSchedule(valveId, time, duration) {
    fetch('/api/schedules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ valve_id: valveId, time, duration })
    })
    .then(response => {
        if (response.ok) {
            alert('تمت إضافة الجدول بنجاح');
            location.reload();
        }
    });
}