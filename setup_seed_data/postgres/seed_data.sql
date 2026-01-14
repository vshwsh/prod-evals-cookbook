-- Seed data for Acme Corp analytics database
-- Focused dataset for demonstration purposes

-- Clear existing data
TRUNCATE customers, monthly_revenue, support_tickets, refunds, employees RESTART IDENTITY CASCADE;

-- =============================================================================
-- EMPLOYEES (key people referenced in documents)
-- =============================================================================
INSERT INTO employees (name, email, department, role, start_date, manager_id, status) VALUES
('Sarah Chen', 'sarah.chen@acme-corp.com', 'Engineering', 'VP Engineering', '2020-03-15', NULL, 'active'),
('Marcus Williams', 'marcus.williams@acme-corp.com', 'Product', 'CPO', '2020-01-10', NULL, 'active'),
('Jennifer Martinez', 'jennifer.martinez@acme-corp.com', 'Sales', 'CRO', '2020-06-01', NULL, 'active'),
('David Kim', 'david.kim@acme-corp.com', 'Customer Success', 'VP Customer Success', '2020-09-01', NULL, 'active'),
('Rachel Thompson', 'rachel.thompson@acme-corp.com', 'People Ops', 'VP People', '2021-01-15', NULL, 'active'),
('James Liu', 'james.liu@acme-corp.com', 'Engineering', 'Staff Engineer', '2021-02-01', 1, 'active'),
('Priya Patel', 'priya.patel@acme-corp.com', 'Engineering', 'Senior Engineer', '2021-06-15', 1, 'active'),
('Alex Rivera', 'alex.rivera@acme-corp.com', 'Engineering', 'Mobile Lead', '2021-04-01', 1, 'active'),
('Emily Watson', 'emily.watson@acme-corp.com', 'Engineering', 'Engineering Manager', '2021-03-01', 1, 'active'),
('Michael Brown', 'michael.brown@acme-corp.com', 'Product', 'Senior PM', '2021-07-01', 2, 'active'),
('Lisa Park', 'lisa.park@acme-corp.com', 'Sales', 'Enterprise AE', '2021-09-01', 3, 'active');

-- =============================================================================
-- CUSTOMERS (mix of tiers and statuses)
-- =============================================================================

-- Enterprise customers
INSERT INTO customers (name, domain, plan_tier, industry, employee_count, signup_date, status, mrr, region) VALUES
('TechCorp Inc', 'techcorp.com', 'enterprise', 'Technology', 5000, '2022-03-15', 'active', 8500.00, 'North America'),
('Global Finance Ltd', 'globalfinance.com', 'enterprise', 'Financial Services', 12000, '2022-06-01', 'active', 12000.00, 'Europe'),
('HealthFirst', 'healthfirst.io', 'enterprise', 'Healthcare', 3000, '2022-09-10', 'active', 6500.00, 'North America'),
('Retail Giants', 'retailgiants.com', 'enterprise', 'Retail', 8000, '2023-01-15', 'active', 9200.00, 'North America'),
('AutoMakers Corp', 'automakers.com', 'enterprise', 'Manufacturing', 15000, '2023-04-01', 'active', 15000.00, 'Europe'),
('DataDriven Analytics', 'datadriven.io', 'enterprise', 'Technology', 800, '2023-07-20', 'active', 4200.00, 'North America'),
('EduLearn Online', 'edulearn.com', 'enterprise', 'Education', 500, '2023-10-05', 'active', 3800.00, 'Asia Pacific'),
('Globex Corporation', 'globex.com', 'enterprise', 'Conglomerate', 25000, '2022-01-10', 'active', 18500.00, 'North America');

-- Professional customers
INSERT INTO customers (name, domain, plan_tier, industry, employee_count, signup_date, status, mrr, region) VALUES
('StartupXYZ', 'startupxyz.io', 'professional', 'Technology', 45, '2023-02-20', 'active', 840.00, 'North America'),
('Creative Agency Co', 'creativeagency.co', 'professional', 'Marketing', 30, '2023-05-15', 'active', 560.00, 'Europe'),
('LegalEase', 'legalease.law', 'professional', 'Legal', 80, '2023-08-01', 'active', 1400.00, 'North America'),
('ConsultPro', 'consultpro.com', 'professional', 'Consulting', 120, '2023-11-10', 'active', 2100.00, 'North America'),
('BioTech Innovations', 'biotechinno.com', 'professional', 'Healthcare', 65, '2024-01-15', 'active', 1120.00, 'Europe'),
('MediaFlow', 'mediaflow.tv', 'professional', 'Media', 40, '2024-03-01', 'active', 720.00, 'North America'),
('FinanceHub', 'financehub.io', 'professional', 'Financial Services', 55, '2024-05-20', 'active', 980.00, 'Asia Pacific'),
('CloudNine Solutions', 'cloudnine.tech', 'professional', 'Technology', 90, '2024-07-01', 'active', 1580.00, 'North America');

-- Starter customers
INSERT INTO customers (name, domain, plan_tier, industry, employee_count, signup_date, status, mrr, region) VALUES
('SmallBiz LLC', 'smallbiz.com', 'starter', 'Retail', 12, '2024-01-10', 'active', 144.00, 'North America'),
('Freelance United', 'freelanceunited.co', 'starter', 'Professional Services', 8, '2024-02-15', 'active', 96.00, 'Europe'),
('LocalShop', 'localshop.biz', 'starter', 'Retail', 5, '2024-04-01', 'active', 60.00, 'North America'),
('DesignStudio', 'designstudio.art', 'starter', 'Design', 6, '2024-06-10', 'active', 72.00, 'Europe'),
('TechStartup', 'techstartup.dev', 'starter', 'Technology', 10, '2024-08-01', 'active', 120.00, 'North America'),
('MarketingMavens', 'marketingmavens.co', 'starter', 'Marketing', 7, '2024-09-15', 'active', 84.00, 'Asia Pacific');

-- Churned customers
INSERT INTO customers (name, domain, plan_tier, industry, employee_count, signup_date, status, mrr, region) VALUES
('FailedStartup Inc', 'failedstartup.com', 'professional', 'Technology', 25, '2023-06-01', 'churned', 0, 'North America'),
('BudgetCuts Corp', 'budgetcuts.biz', 'starter', 'Retail', 15, '2023-09-01', 'churned', 0, 'Europe'),
('OldSchool Ltd', 'oldschool.com', 'professional', 'Manufacturing', 200, '2022-12-01', 'churned', 0, 'North America'),
('TightBudget LLC', 'tightbudget.co', 'enterprise', 'Financial Services', 500, '2023-03-01', 'churned', 0, 'Europe');

-- =============================================================================
-- MONTHLY REVENUE (2024 data)
-- =============================================================================
INSERT INTO monthly_revenue (month, mrr, new_mrr, expansion_mrr, contraction_mrr, churned_mrr, customer_count) VALUES
('2024-01-01', 1250000, 85000, 42000, 12000, 28000, 2150),
('2024-02-01', 1285000, 72000, 38000, 8000, 22000, 2180),
('2024-03-01', 1320000, 95000, 45000, 15000, 30000, 2220),
('2024-04-01', 1358000, 78000, 52000, 10000, 25000, 2265),
('2024-05-01', 1395000, 82000, 48000, 12000, 28000, 2310),
('2024-06-01', 1428000, 68000, 55000, 8000, 20000, 2345),
('2024-07-01', 1465000, 92000, 42000, 14000, 32000, 2380),
('2024-08-01', 1498000, 75000, 48000, 10000, 24000, 2410),
('2024-09-01', 1535000, 88000, 52000, 12000, 26000, 2455),
('2024-10-01', 1572000, 95000, 58000, 8000, 30000, 2495),
('2024-11-01', 1610000, 82000, 62000, 14000, 28000, 2530),
('2024-12-01', 1648000, 78000, 55000, 10000, 22000, 2560);

-- =============================================================================
-- SUPPORT TICKETS (recent samples)
-- =============================================================================
INSERT INTO support_tickets (customer_id, created_at, resolved_at, category, priority, status, subject, csat_score, first_response_minutes, resolution_minutes) VALUES
(1, '2024-12-01 09:30:00', '2024-12-01 11:45:00', 'Technical', 'P2', 'resolved', 'API rate limiting causing errors', 4, 15, 135),
(2, '2024-12-02 14:00:00', '2024-12-02 16:30:00', 'Billing', 'P3', 'resolved', 'Invoice discrepancy question', 5, 30, 150),
(3, '2024-12-03 10:15:00', '2024-12-03 10:45:00', 'Technical', 'P1', 'resolved', 'Login failures for SSO users', 5, 5, 30),
(4, '2024-12-04 16:45:00', '2024-12-05 09:00:00', 'Feature Request', 'P4', 'resolved', 'Request for custom export format', 4, 60, 960),
(5, '2024-12-05 11:30:00', NULL, 'Technical', 'P2', 'in_progress', 'Integration sync delays', NULL, 20, NULL),
(6, '2024-12-06 08:00:00', '2024-12-06 09:15:00', 'Account', 'P3', 'resolved', 'Add new team members to account', 5, 10, 75),
(1, '2024-12-07 13:20:00', '2024-12-07 14:00:00', 'Technical', 'P2', 'resolved', 'Webhook delivery failures', 4, 12, 40),
(8, '2024-12-08 09:45:00', '2024-12-08 15:30:00', 'Billing', 'P2', 'resolved', 'Upgrade to enterprise plan', 5, 25, 345),
(9, '2024-12-09 14:30:00', NULL, 'Technical', 'P3', 'open', 'Mobile app performance issues', NULL, NULL, NULL),
(10, '2024-12-10 10:00:00', '2024-12-10 11:30:00', 'Account', 'P3', 'resolved', 'Password reset not working', 4, 18, 90);

-- =============================================================================
-- REFUNDS (for multi-tool query demo: policy + SQL)
-- =============================================================================
INSERT INTO refunds (customer_id, amount, reason, processed_at, approved_by, quarter) VALUES
(23, 450.00, '30-day cancellation', '2024-10-05 14:30:00', 'CS Rep', '2024-Q4'),
(24, 180.00, '30-day cancellation', '2024-10-12 09:15:00', 'CS Rep', '2024-Q4'),
(25, 2400.00, 'SLA breach compensation', '2024-10-20 16:00:00', 'VP Customer Success', '2024-Q4'),
(22, 850.00, 'Pro-rata annual cancellation', '2024-11-02 11:30:00', 'CS Manager', '2024-Q4'),
(21, 320.00, 'Billing error', '2024-11-15 14:00:00', 'CS Rep', '2024-Q4'),
(20, 1200.00, 'Pro-rata annual cancellation', '2024-11-28 10:45:00', 'CS Manager', '2024-Q4'),
(19, 550.00, '30-day cancellation', '2024-12-03 09:00:00', 'CS Rep', '2024-Q4'),
(18, 280.00, 'Billing error', '2024-12-10 15:30:00', 'CS Rep', '2024-Q4');

-- =============================================================================
-- Helpful views for common queries
-- =============================================================================
CREATE OR REPLACE VIEW v_active_customers_by_tier AS
SELECT 
    plan_tier,
    COUNT(*) as customer_count,
    SUM(mrr) as total_mrr,
    ROUND(AVG(mrr), 2) as avg_mrr
FROM customers
WHERE status = 'active'
GROUP BY plan_tier
ORDER BY total_mrr DESC;

CREATE OR REPLACE VIEW v_refunds_by_quarter AS
SELECT 
    quarter,
    COUNT(*) as refund_count,
    SUM(amount) as total_amount,
    ROUND(AVG(amount), 2) as avg_amount
FROM refunds
GROUP BY quarter
ORDER BY quarter DESC;
