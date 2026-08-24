from database.database import get_connection


conn = get_connection()

cursor = conn.cursor()

print("Rebuilding production_orders table...")

cursor.execute("""
ALTER TABLE production_orders
RENAME TO production_orders_old
""")

cursor.execute("""
CREATE TABLE production_orders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id TEXT,

    garment_name TEXT,

    design_name TEXT,

    client_name TEXT,

    client TEXT,

    category TEXT,

    fabric TEXT,

    quantity INTEGER DEFAULT 1,

    status TEXT DEFAULT 'Pending',

    priority TEXT DEFAULT 'Normal',

    deadline TEXT,

    due_date TEXT,

    assigned_to TEXT,

    notes TEXT,

    progress INTEGER DEFAULT 0,

    measurement_profile_id INTEGER,

    tech_pack_id INTEGER,

    design_id INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT INTO production_orders (

    id,
    user_id,
    garment_name,
    design_name,
    client_name,
    client,
    category,
    fabric,
    quantity,
    status,
    priority,
    deadline,
    due_date,
    assigned_to,
    notes,
    progress,
    measurement_profile_id,
    tech_pack_id,
    design_id,
    created_at,
    updated_at

)

SELECT

    id,
    user_id,

    COALESCE(
        garment_name,
        design_name,
        'Untitled Production'
    ),

    COALESCE(
        design_name,
        garment_name,
        'Untitled Production'
    ),

    COALESCE(
        client_name,
        client,
        'No Client'
    ),

    COALESCE(
        client,
        client_name,
        'No Client'
    ),

    category,

    fabric,

    COALESCE(
        quantity,
        1
    ),

    COALESCE(
        status,
        'Pending'
    ),

    COALESCE(
        priority,
        'Normal'
    ),

    deadline,

    COALESCE(
        due_date,
        deadline
    ),

    COALESCE(
        assigned_to,
        'Unassigned'
    ),

    notes,

    COALESCE(
        progress,
        0
    ),

    measurement_profile_id,

    tech_pack_id,

    design_id,

    created_at,

    updated_at

FROM production_orders_old
""")

cursor.execute("""
DROP TABLE production_orders_old
""")

conn.commit()

conn.close()

print("Production database fixed successfully.")