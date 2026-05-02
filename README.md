# Capital Projects Dashboard

A SQL-based capital program analytics project simulating owner-side reporting for a portfolio of data center construction projects. Built to reflect real PMIS data structures and the analytical questions owner program management teams actually ask.

## Overview

This project models how construction data moves from a PMIS (like Procore or e-Builder) into an analytical layer for executive reporting. It includes a relational PostgreSQL database, a synthetic dataset generated with Python, six analytical SQL views, and an interactive Tableau dashboard.

## Live Dashboard

[View on GitHub Pages](https://catalinavalenciad.github.io/capital-projects-dashboard/)

[View on Tableau Public](https://public.tableau.com/views/CapitalProjectsDashboard/Dashboard1)

## Tech Stack

- **PostgreSQL** — relational database and analytical views
- **Python** (pandas, faker) — synthetic data generation
- **Tableau Public** — interactive dashboard
- **VS Code** — development environment

## Repository Structure

```
capital-projects-dashboard/
├── data/
│   └── sources.md
├── sql/
│   ├── schema.sql
│   ├── queries.sql
│   └── views.sql
├── scripts/
│   └── generate_data.py
├── query_outputs/
│   ├── budget_variance.csv
│   ├── change_order_impact.csv
│   ├── rfi_summary.csv
│   ├── change_event_breakdown.csv
│   ├── spend_over_time.csv
│   └── submittal_status_detail.csv
├── docs/
│   └── index.html
└── README.md
```

## Database Schema

Six tables modeled after real PMIS data structures:

| Table | Rows | Description |
|---|---|---|
| projects | 10 | Master project list |
| contracts | 37 | GC and subcontracts |
| change_events | 102 | COs, CCDs, ASIs, CORs, Field Orders |
| rfis | 172 | Requests for information |
| submittals | 130 | Shop drawings, product data, samples |
| budget_tracking | 171 | Monthly planned vs actual spend |

## Running the Project

1. Install PostgreSQL and create a database called `capital_projects`
2. Run `sql/schema.sql` to create the tables
3. Run `scripts/generate_data.py` to generate the CSV data files
4. Import each CSV into its corresponding table using pgAdmin
5. Run `sql/views.sql` to create the analytical views
6. Connect Tableau to PostgreSQL or use the CSVs in `query_outputs/`
