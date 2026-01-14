-- Acme Corp Analytics Database Schema
-- This schema supports SQL queries about customers, revenue, and support

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    plan_tier VARCHAR(50) NOT NULL CHECK (plan_tier IN ('free', 'starter', 'professional', 'enterprise')),
    industry VARCHAR(100),
    employee_count INTEGER,
    signup_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'churned', 'trial')),
    mrr DECIMAL(10, 2) DEFAULT 0,
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monthly revenue metrics
CREATE TABLE IF NOT EXISTS monthly_revenue (
    id SERIAL PRIMARY KEY,
    month DATE NOT NULL UNIQUE,
    mrr DECIMAL(12, 2) NOT NULL,
    new_mrr DECIMAL(12, 2) DEFAULT 0,
    expansion_mrr DECIMAL(12, 2) DEFAULT 0,
    contraction_mrr DECIMAL(12, 2) DEFAULT 0,
    churned_mrr DECIMAL(12, 2) DEFAULT 0,
    customer_count INTEGER NOT NULL
);

-- Support tickets
CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    category VARCHAR(100) NOT NULL,
    priority VARCHAR(10) CHECK (priority IN ('P1', 'P2', 'P3', 'P4')),
    status VARCHAR(50) CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    subject VARCHAR(500),
    csat_score INTEGER CHECK (csat_score >= 1 AND csat_score <= 5),
    first_response_minutes INTEGER,
    resolution_minutes INTEGER
);

-- Refunds tracking (for the multi-tool query demo)
CREATE TABLE IF NOT EXISTS refunds (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount DECIMAL(10, 2) NOT NULL,
    reason VARCHAR(255),
    processed_at TIMESTAMP NOT NULL,
    approved_by VARCHAR(100),
    quarter VARCHAR(10) -- e.g., '2024-Q4'
);

-- Employees (internal)
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    manager_id INTEGER REFERENCES employees(id),
    status VARCHAR(50) DEFAULT 'active'
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_customers_plan_tier ON customers(plan_tier);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
CREATE INDEX IF NOT EXISTS idx_customers_signup_date ON customers(signup_date);
CREATE INDEX IF NOT EXISTS idx_support_tickets_customer ON support_tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_created ON support_tickets(created_at);
CREATE INDEX IF NOT EXISTS idx_refunds_quarter ON refunds(quarter);
CREATE INDEX IF NOT EXISTS idx_refunds_processed ON refunds(processed_at);
