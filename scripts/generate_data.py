import pandas as pd
import random
from faker import Faker
from datetime import date, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

# Reference data
project_types = ['New Construction', 'Expansion', 'Renovation', 'Tenant Improvement']
locations = [
    'Austin, TX', 'Dallas, TX', 'Phoenix, AZ', 'Atlanta, GA',
    'Chicago, IL', 'Seattle, WA', 'Denver, CO', 'Charlotte, NC',
    'Las Vegas, NV', 'Richmond, VA'
]
statuses = ['Active', 'Closed', 'On Hold']
project_managers = [
    'James Holloway', 'Maria Reyes', 'David Kim',
    'Sandra Osei', 'Chris Patel'
]
contract_types = ['General Contract', 'Design-Build', 'CM at Risk', 'Subcontract', 'Commissioning']
contractor_names = [
    'Turner Construction', 'Hensel Phelps', 'DPR Construction',
    'Whiting-Turner', 'Holder Construction', 'JE Dunn',
    'McCarthy Building Companies', 'Skanska', 'Suffolk Construction',
    'Balfour Beatty'
]
event_types = ['Change Order', 'CCD', 'ASI', 'Field Order', 'COR']
reasons = [
    'Unforeseen Conditions', 'Owner Request', 'Design Error',
    'Value Engineering', 'Code Compliance', 'Scope Addition'
]
change_statuses = ['Approved', 'Pending', 'Rejected', 'Under Review']
submittal_types = ['Shop Drawing', 'Product Data', 'Sample', 'Operation & Maintenance Manual']
submittal_statuses = ['Approved', 'Approved as Noted', 'Revise and Resubmit', 'Rejected', 'Pending']
rfi_statuses = ['Open', 'Closed', 'Pending']

# Generate projects
projects = []
for i in range(1, 11):
    start = fake.date_between(start_date=date(2020, 1, 1), end_date=date(2023, 6, 1))
    end = start + timedelta(days=random.randint(365, 900))
    projects.append({
        'project_id': i,
        'project_name': f'{random.choice(locations).split(",")[0]} Data Center {random.choice(["Phase 1", "Phase 2", "Expansion", "Build 1"])}',
        'location': random.choice(locations),
        'project_type': random.choice(project_types),
        'total_budget': round(random.uniform(5000000, 80000000), 2),
        'construction_start': start,
        'substantial_completion': end,
        'status': random.choice(statuses),
        'project_manager': random.choice(project_managers)
    })

df_projects = pd.DataFrame(projects)
df_projects.to_csv('projects.csv', index=False)
print('projects.csv created')

# Generate contracts
contracts = []
contract_id = 1
for project in projects:
    num_contracts = random.randint(3, 5)
    for _ in range(num_contracts):
        contracts.append({
            'contract_id': contract_id,
            'project_id': project['project_id'],
            'contractor_name': random.choice(contractor_names),
            'contract_type': random.choice(contract_types),
            'contract_value': round(random.uniform(500000, project['total_budget'] * 0.6), 2),
            'executed_date': project['construction_start'],
            'scheduled_completion': project['substantial_completion'],
            'status': project['status']
        })
        contract_id += 1

df_contracts = pd.DataFrame(contracts)
df_contracts.to_csv('contracts.csv', index=False)
print('contracts.csv created')

# Generate change_events
change_events = []
change_event_id = 1
for project in projects:
    project_contracts = [c for c in contracts if c['project_id'] == project['project_id']]
    for _ in range(random.randint(8, 12)):
        contract = random.choice(project_contracts)
        change_events.append({
            'change_event_id': change_event_id,
            'project_id': project['project_id'],
            'contract_id': contract['contract_id'],
            'event_type': random.choice(event_types),
            'description': fake.sentence(nb_words=8),
            'reason': random.choice(reasons),
            'cost_impact': round(random.uniform(-50000, 500000), 2),
            'schedule_impact_days': random.randint(-5, 45),
            'date_submitted': fake.date_between(
                start_date=project['construction_start'],
                end_date=project['substantial_completion']
            ),
            'status': random.choice(change_statuses)
        })
        change_event_id += 1

df_change_events = pd.DataFrame(change_events)
df_change_events.to_csv('change_events.csv', index=False)
print('change_events.csv created')

# Generate rfis
rfis = []
rfi_id = 1
for project in projects:
    project_contracts = [c for c in contracts if c['project_id'] == project['project_id']]
    for _ in range(random.randint(15, 20)):
        contract = random.choice(project_contracts)
        date_submitted = fake.date_between(
            start_date=project['construction_start'],
            end_date=project['substantial_completion']
        )
        date_due = date_submitted + timedelta(days=14)
        responded = random.choice([True, False])
        date_responded = date_due + timedelta(days=random.randint(0, 30)) if responded else None
        rfis.append({
            'rfi_id': rfi_id,
            'project_id': project['project_id'],
            'contract_id': contract['contract_id'],
            'rfi_number': f'RFI-{str(rfi_id).zfill(4)}',
            'subject': fake.sentence(nb_words=6),
            'submitted_by': random.choice(contractor_names),
            'date_submitted': date_submitted,
            'date_due': date_due,
            'date_responded': date_responded,
            'status': random.choice(rfi_statuses),
            'led_to_change_event': random.choice([True, False])
        })
        rfi_id += 1

df_rfis = pd.DataFrame(rfis)
df_rfis.to_csv('rfis.csv', index=False)
print('rfis.csv created')

# Generate submittals
submittals = []
submittal_id = 1
for project in projects:
    project_contracts = [c for c in contracts if c['project_id'] == project['project_id']]
    for _ in range(random.randint(10, 15)):
        contract = random.choice(project_contracts)
        date_submitted = fake.date_between(
            start_date=project['construction_start'],
            end_date=project['substantial_completion']
        )
        date_due = date_submitted + timedelta(days=14)
        date_reviewed = date_due + timedelta(days=random.randint(0, 21))
        submittals.append({
            'submittal_id': submittal_id,
            'project_id': project['project_id'],
            'contract_id': contract['contract_id'],
            'submittal_number': f'SUB-{str(submittal_id).zfill(4)}',
            'submittal_type': random.choice(submittal_types),
            'description': fake.sentence(nb_words=6),
            'submitted_by': random.choice(contractor_names),
            'date_submitted': date_submitted,
            'date_due': date_due,
            'date_reviewed': date_reviewed,
            'status': random.choice(submittal_statuses)
        })
        submittal_id += 1

df_submittals = pd.DataFrame(submittals)
df_submittals.to_csv('submittals.csv', index=False)
print('submittals.csv created')

# Generate budget_tracking
budget_tracking = []
budget_id = 1
for project in projects:
    start = project['construction_start']
    end = project['substantial_completion']
    total_budget = project['total_budget']
    current = start.replace(day=1)
    cumulative_planned = 0
    cumulative_actual = 0
    while current <= end:
        planned = round(random.uniform(total_budget * 0.03, total_budget * 0.08), 2)
        actual = round(planned * random.uniform(0.85, 1.20), 2)
        cumulative_planned += planned
        cumulative_actual += actual
        budget_tracking.append({
            'budget_id': budget_id,
            'project_id': project['project_id'],
            'period_date': current,
            'planned_spend': planned,
            'actual_spend': actual,
            'cumulative_planned': round(cumulative_planned, 2),
            'cumulative_actual': round(cumulative_actual, 2)
        })
        budget_id += 1
        month = current.month + 1
        year = current.year + (month > 12)
        month = month if month <= 12 else 1
        current = current.replace(year=year, month=month)

df_budget = pd.DataFrame(budget_tracking)
df_budget.to_csv('budget_tracking.csv', index=False)
print('budget_tracking.csv created')

print('All CSVs created successfully')