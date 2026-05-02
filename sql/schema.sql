-- Capital Projects: Data Center Portfolio Analysis
-- Modeled after real PMIS data structures (Procore, e-Builder)

-- Projects table: master list of capital projects in the program
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    project_type VARCHAR(100),
    total_budget NUMERIC(15,2),
    construction_start DATE,
    substantial_completion DATE,
    status VARCHAR(50),
    project_manager VARCHAR(255)
);

CREATE TABLE contracts (
    contract_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id),
    contractor_name VARCHAR(255) NOT NULL,
    contract_type VARCHAR(100),
    contract_value NUMERIC(15,2),
    executed_date DATE,
    scheduled_completion DATE,
    status VARCHAR(50)
);

CREATE TABLE change_events (
    change_event_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id),
    contract_id INT REFERENCES contracts(contract_id),
    event_type VARCHAR(100),
    description TEXT,
    reason VARCHAR(100),
    cost_impact NUMERIC(15,2),
    schedule_impact_days INT,
    date_submitted DATE,
    status VARCHAR(50)
);

CREATE TABLE rfis (
    rfi_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id),
    contract_id INT REFERENCES contracts(contract_id),
    rfi_number VARCHAR(50),
    subject VARCHAR(255),
    submitted_by VARCHAR(255),
    date_submitted DATE,
    date_due DATE,
    date_responded DATE,
    status VARCHAR(50),
    led_to_change_event BOOLEAN
);

CREATE TABLE submittals (
    submittal_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id),
    contract_id INT REFERENCES contracts(contract_id),
    submittal_number VARCHAR(50),
    submittal_type VARCHAR(100),
    description VARCHAR(255),
    submitted_by VARCHAR(255),
    date_submitted DATE,
    date_due DATE,
    date_reviewed DATE,
    status VARCHAR(50)
);

CREATE TABLE budget_tracking (
    budget_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(project_id),
    period_date DATE,
    planned_spend NUMERIC(15,2),
    actual_spend NUMERIC(15,2),
    cumulative_planned NUMERIC(15,2),
    cumulative_actual NUMERIC(15,2)
);