-- EV Fleet Management Database Schema
-- PostgreSQL 15+

-- Vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE NOT NULL,
    model VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    year_manufactured INT,
    registration_number VARCHAR(20) UNIQUE,
    current_soh DECIMAL(5,2) DEFAULT 85.00,
    total_cycles INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'operational',
    location_latitude DECIMAL(10,8),
    location_longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_status (status)
);

-- Battery health records (time-series)
CREATE TABLE IF NOT EXISTS battery_health_records (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    soh_percent DECIMAL(5,2),
    charge_cycles INT,
    voltage_v DECIMAL(6,3),
    current_a DECIMAL(6,2),
    temperature_c DECIMAL(5,2),
    risk_level VARCHAR(20),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    INDEX idx_vehicle_timestamp (vehicle_id, recorded_at)
);

-- Suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    supplier_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    material_type VARCHAR(100),
    risk_score DECIMAL(3,2),
    concentration_index DECIMAL(6,4),
    lead_time_days INT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_supplier_id (supplier_id),
    INDEX idx_material (material_type)
);

-- Supply chain events
CREATE TABLE IF NOT EXISTS supply_chain_events (
    id SERIAL PRIMARY KEY,
    supplier_id VARCHAR(50),
    event_type VARCHAR(100),
    severity VARCHAR(20),
    description TEXT,
    impact_estimated DECIMAL(8,2),
    event_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    INDEX idx_severity (severity),
    INDEX idx_date (event_date)
);

-- Fleet analytics
CREATE TABLE IF NOT EXISTS fleet_analytics (
    id SERIAL PRIMARY KEY,
    metric_date DATE,
    total_vehicles INT,
    average_soh DECIMAL(5,2),
    vehicles_high_risk INT,
    vehicles_medium_risk INT,
    vehicles_healthy INT,
    electrification_readiness_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_metric_date (metric_date)
);

-- Anomalies detected
CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50),
    anomaly_type VARCHAR(100),
    confidence_score DECIMAL(3,2),
    severity VARCHAR(20),
    description TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_severity (severity)
);

-- Predictions and forecasts
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50),
    prediction_type VARCHAR(100),
    forecast_date DATE,
    predicted_value DECIMAL(10,4),
    confidence_interval_low DECIMAL(10,4),
    confidence_interval_high DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    INDEX idx_vehicle_type (vehicle_id, prediction_type)
);

-- Indexes for performance
CREATE INDEX idx_battery_health_timestamp ON battery_health_records(recorded_at DESC);
CREATE INDEX idx_supply_events_severity ON supply_chain_events(severity);
CREATE INDEX idx_anomalies_date ON anomalies(detected_at DESC);
CREATE INDEX idx_predictions_date ON predictions(forecast_date);

-- Sample data insertion (optional, for testing)
INSERT INTO vehicles (vehicle_id, model, manufacturer, year_manufactured, current_soh, total_cycles, status)
VALUES 
    ('VEH001', 'Nexon EV', 'Tata', 2023, 92.5, 450, 'operational'),
    ('VEH002', 'XUV500', 'Mahindra', 2023, 89.3, 320, 'operational'),
    ('VEH003', 'Song Plus DM', 'BYD', 2023, 95.1, 200, 'operational'),
    ('VEH004', 'ZS EV', 'MG', 2022, 87.2, 580, 'operational'),
    ('VEH005', 'e-UP', 'Volkswagen', 2022, 81.5, 750, 'maintenance')
ON CONFLICT DO NOTHING;

INSERT INTO suppliers (supplier_id, name, country, material_type, risk_score, concentration_index, lead_time_days, status)
VALUES 
    ('SUP001', 'CATL', 'China', 'Lithium', 0.65, 0.45, 60, 'active'),
    ('SUP002', 'Albemarle', 'USA', 'Lithium', 0.45, 0.32, 45, 'active'),
    ('SUP003', 'Ganfeng', 'China', 'Lithium', 0.72, 0.38, 75, 'active'),
    ('SUP004', 'Glencore', 'Australia', 'Cobalt', 0.55, 0.48, 50, 'active')
ON CONFLICT DO NOTHING;
