#!/usr/bin/env python3

import mysql.connector
import configparser
import sys
import hashlib
import os
import binascii

class GuacamoleDB:
    def __init__(self, config_file='db_config.ini', debug=False):
        self.debug = debug
        self.db_config = self.read_config(config_file)
        self.conn = self.connect_db()
        self.cursor = self.conn.cursor()

    def debug_print(self, *args, **kwargs):
        """Print debug messages if debug mode is enabled"""
        if self.debug:
            print("[DEBUG]", *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            try:
                # Always commit unless there was an exception
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            finally:
                self.conn.close()

    @staticmethod
    def read_config(config_file):
        config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            print(f"Error: Config file not found: {config_file}")
            print("Please create a config file at ~/.guacaman.ini with the following format:")
            print("[mysql]")
            print("host = your_mysql_host")
            print("user = your_mysql_user")
            print("password = your_mysql_password")
            print("database = your_mysql_database")
            sys.exit(1)
            
        try:
            config.read(config_file)
            if 'mysql' not in config:
                print(f"Error: Missing [mysql] section in config file: {config_file}")
                sys.exit(1)
                
            required_keys = ['host', 'user', 'password', 'database']
            missing_keys = [key for key in required_keys if key not in config['mysql']]
            if missing_keys:
                print(f"Error: Missing required keys in [mysql] section: {', '.join(missing_keys)}")
                print(f"Config file: {config_file}")
                sys.exit(1)
                
            return {
                'host': config['mysql']['host'],
                'user': config['mysql']['user'],
                'password': config['mysql']['password'],
                'database': config['mysql']['database']
            }
        except Exception as e:
            print(f"Error reading config file {config_file}: {str(e)}")
            sys.exit(1)

    def connect_db(self):
        try:
            return mysql.connector.connect(
                **self.db_config,
                charset='utf8mb4',
                collation='utf8mb4_general_ci'
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def list_users(self):
        try:
            self.cursor.execute("""
                SELECT name 
                FROM guacamole_entity 
                WHERE type = 'USER' 
                ORDER BY name
            """)
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error listing users: {e}")
            raise

    def list_groups(self):
        try:
            self.cursor.execute("""
                SELECT name 
                FROM guacamole_entity 
                WHERE type = 'USER_GROUP' 
                ORDER BY name
            """)
            return [row[0] for row in self.cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error listing groups: {e}")
            raise

    def group_exists(self, group_name):
        """Check if a group with the given name exists"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM guacamole_entity 
                WHERE name = %s AND type = 'USER_GROUP'
            """, (group_name,))
            return self.cursor.fetchone()[0] > 0
        except mysql.connector.Error as e:
            print(f"Error checking group existence: {e}")
            raise

    def get_group_id(self, group_name):
        try:
            self.cursor.execute("""
                SELECT user_group_id 
                FROM guacamole_user_group g
                JOIN guacamole_entity e ON g.entity_id = e.entity_id
                WHERE e.name = %s AND e.type = 'USER_GROUP'
            """, (group_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                raise Exception(f"Group '{group_name}' not found")
        except mysql.connector.Error as e:
            print(f"Error getting group ID: {e}")
            raise

    def user_exists(self, username):
        """Check if a user with the given name exists"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM guacamole_entity 
                WHERE name = %s AND type = 'USER'
            """, (username,))
            return self.cursor.fetchone()[0] > 0
        except mysql.connector.Error as e:
            print(f"Error checking user existence: {e}")
            raise

    def delete_existing_user(self, username):
        try:
            if not self.user_exists(username):
                raise ValueError(f"User '{username}' doesn't exist")
                
            self.debug_print(f"Deleting user: {username}")
            # Delete user group permissions first
            self.cursor.execute("""
                DELETE FROM guacamole_user_group_permission 
                WHERE entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER'
                )
            """, (username,))

            # Delete user group memberships
            self.cursor.execute("""
                DELETE FROM guacamole_user_group_member 
                WHERE member_entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER'
                )
            """, (username,))

            # Delete user permissions
            self.cursor.execute("""
                DELETE FROM guacamole_connection_permission 
                WHERE entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER'
                )
            """, (username,))

            # Delete user
            self.cursor.execute("""
                DELETE FROM guacamole_user 
                WHERE entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER'
                )
            """, (username,))

            # Delete entity
            self.cursor.execute("""
                DELETE FROM guacamole_entity 
                WHERE name = %s AND type = 'USER'
            """, (username,))

        except mysql.connector.Error as e:
            print(f"Error deleting existing user: {e}")
            raise

    def delete_existing_group(self, group_name):
        try:
            self.debug_print(f"Deleting group: {group_name}")
            # Delete group memberships
            self.cursor.execute("""
                DELETE FROM guacamole_user_group_member 
                WHERE user_group_id IN (
                    SELECT user_group_id FROM guacamole_user_group 
                    WHERE entity_id IN (
                        SELECT entity_id FROM guacamole_entity 
                        WHERE name = %s AND type = 'USER_GROUP'
                    )
                )
            """, (group_name,))

            # Delete group permissions
            self.cursor.execute("""
                DELETE FROM guacamole_connection_permission 
                WHERE entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER_GROUP'
                )
            """, (group_name,))

            # Delete user group
            self.cursor.execute("""
                DELETE FROM guacamole_user_group 
                WHERE entity_id IN (
                    SELECT entity_id FROM guacamole_entity 
                    WHERE name = %s AND type = 'USER_GROUP'
                )
            """, (group_name,))

            # Delete entity
            self.cursor.execute("""
                DELETE FROM guacamole_entity 
                WHERE name = %s AND type = 'USER_GROUP'
            """, (group_name,))

        except mysql.connector.Error as e:
            print(f"Error deleting existing group: {e}")
            raise

    def delete_existing_connection(self, connection_name):
        try:
            self.debug_print(f"Attempting to delete connection: {connection_name}")
            
            # Get connection_id first
            self.cursor.execute("""
                SELECT connection_id FROM guacamole_connection
                WHERE connection_name = %s
            """, (connection_name,))
            result = self.cursor.fetchone()
            if not result:
                raise ValueError(f"Connection '{connection_name}' doesn't exist")
            connection_id = result[0]
            self.debug_print(f"Found connection_id: {connection_id}")

            # Delete connection history
            self.debug_print("Deleting connection history...")
            self.cursor.execute("""
                DELETE FROM guacamole_connection_history
                WHERE connection_id = %s
            """, (connection_id,))

            # Delete connection parameters
            self.debug_print("Deleting connection parameters...")
            self.cursor.execute("""
                DELETE FROM guacamole_connection_parameter
                WHERE connection_id = %s
            """, (connection_id,))

            # Delete connection permissions
            self.debug_print("Deleting connection permissions...")
            self.cursor.execute("""
                DELETE FROM guacamole_connection_permission
                WHERE connection_id = %s
            """, (connection_id,))

            # Finally delete the connection
            self.debug_print("Deleting connection...")
            self.cursor.execute("""
                DELETE FROM guacamole_connection
                WHERE connection_id = %s
            """, (connection_id,))

            # Commit the transaction
            self.debug_print("Committing transaction...")
            self.conn.commit()
            self.debug_print(f"Successfully deleted connection '{connection_name}'")

        except mysql.connector.Error as e:
            print(f"Error deleting existing connection: {e}")
            raise

    def create_user(self, username, password):
        try:
            # Generate random 32-byte salt
            salt = os.urandom(32)
            
            # Convert salt to uppercase hex string as Guacamole expects
            salt_hex = binascii.hexlify(salt).upper()
            
            # Create password hash using Guacamole's method: SHA256(password + hex(salt))
            digest = hashlib.sha256(
                password.encode('utf-8') + salt_hex
            ).digest()

            # Get binary representations
            password_hash = digest  # SHA256 hash of (password + hex(salt))
            password_salt = salt    # Original raw bytes salt

            # Create entity
            self.cursor.execute("""
                INSERT INTO guacamole_entity (name, type) 
                VALUES (%s, 'USER')
            """, (username,))

            # Create user with proper binary data
            self.cursor.execute("""
                INSERT INTO guacamole_user 
                    (entity_id, password_hash, password_salt, password_date)
                SELECT 
                    entity_id,
                    %s,
                    %s,
                    NOW()
            FROM guacamole_entity 
            WHERE name = %s AND type = 'USER'
            """, (password_hash, password_salt, username))

        except mysql.connector.Error as e:
            print(f"Error creating user: {e}")
            raise

    def create_group(self, group_name):
        try:
            # Create entity
            self.cursor.execute("""
                INSERT INTO guacamole_entity (name, type) 
                VALUES (%s, 'USER_GROUP')
            """, (group_name,))

            # Create group
            self.cursor.execute("""
                INSERT INTO guacamole_user_group (entity_id, disabled)
                SELECT entity_id, FALSE
                FROM guacamole_entity 
                WHERE name = %s AND type = 'USER_GROUP'
            """, (group_name,))

        except mysql.connector.Error as e:
            print(f"Error creating group: {e}")
            raise

    def add_user_to_group(self, username, group_name):
        try:
            # Get the group ID
            group_id = self.get_group_id(group_name)
            
            # Get the user's entity ID
            self.cursor.execute("""
                SELECT entity_id 
                FROM guacamole_entity 
                WHERE name = %s AND type = 'USER'
            """, (username,))
            user_entity_id = self.cursor.fetchone()[0]

            # Add user to group
            self.cursor.execute("""
                INSERT INTO guacamole_user_group_member 
                (user_group_id, member_entity_id)
                VALUES (%s, %s)
            """, (group_id, user_entity_id))

            # Grant group permissions to user
            self.cursor.execute("""
                INSERT INTO guacamole_user_group_permission
                (entity_id, affected_user_group_id, permission)
                SELECT %s, %s, 'READ'
                FROM dual
                WHERE NOT EXISTS (
                    SELECT 1 FROM guacamole_user_group_permission
                    WHERE entity_id = %s 
                    AND affected_user_group_id = %s 
                    AND permission = 'READ'
                )
            """, (user_entity_id, group_id, user_entity_id, group_id))

        except mysql.connector.Error as e:
            print(f"Error adding user to group: {e}")
            raise

    def get_connection_group_id(self, group_path):
        """Resolve nested connection group path to group_id"""
        try:
            groups = group_path.split('/')
            parent_group_id = None
            
            self.debug_print(f"Resolving group path: {group_path}")
            
            for group_name in groups:
                # CORRECTED SQL - use connection_group_name directly
                sql = """
                    SELECT connection_group_id 
                    FROM guacamole_connection_group
                    WHERE connection_group_name = %s
                """
                params = [group_name]
                
                if parent_group_id is not None:
                    sql += " AND parent_id = %s"
                    params.append(parent_group_id)
                else:
                    sql += " AND parent_id IS NULL"
                    
                sql += " ORDER BY connection_group_id LIMIT 1"
                
                self.debug_print(f"Executing SQL:\n{sql}\nWith params: {params}")
                
                self.cursor.execute(sql, tuple(params))
                
                result = self.cursor.fetchone()
                if not result:
                    raise ValueError(f"Group '{group_name}' not found in path '{group_path}'")
                
                parent_group_id = result[0]
                self.debug_print(f"Found group ID {parent_group_id} for '{group_name}'")
                
            return parent_group_id

        except mysql.connector.Error as e:
            print(f"Error resolving group path: {e}")
            raise

    def connection_exists(self, connection_name):
        """Check if a connection with the given name exists"""
        try:
            self.cursor.execute("""
                SELECT COUNT(*) FROM guacamole_connection
                WHERE connection_name = %s
            """, (connection_name,))
            return self.cursor.fetchone()[0] > 0
        except mysql.connector.Error as e:
            print(f"Error checking connection existence: {e}")
            raise

    def create_vnc_connection(self, connection_name, hostname, port, vnc_password, parent_group_id=None):
        if not all([connection_name, hostname, port]):
            raise ValueError("Missing required connection parameters")
            
        if self.connection_exists(connection_name):
            raise ValueError(f"Connection '{connection_name}' already exists")
            
        try:
            # Create connection
            self.cursor.execute("""
                INSERT INTO guacamole_connection 
                (connection_name, protocol, parent_id)
                VALUES (%s, 'vnc', %s)
            """, (connection_name, parent_group_id))

            # Get connection_id
            self.cursor.execute("""
                SELECT connection_id FROM guacamole_connection
                WHERE connection_name = %s
            """, (connection_name,))
            connection_id = self.cursor.fetchone()[0]

            # Create connection parameters
            params = [
                ('hostname', hostname),
                ('port', port),
                ('password', vnc_password)
            ]

            for param_name, param_value in params:
                self.cursor.execute("""
                    INSERT INTO guacamole_connection_parameter 
                    (connection_id, parameter_name, parameter_value)
                    VALUES (%s, %s, %s)
                """, (connection_id, param_name, param_value))

            return connection_id

        except mysql.connector.Error as e:
            print(f"Error creating VNC connection: {e}")
            raise

    def grant_connection_permission(self, entity_name, entity_type, connection_id, group_path=None):
        try:
            if group_path:
                self.debug_print(f"Processing group path: {group_path}")
                parent_group_id = self.get_connection_group_id(group_path)
                
                self.debug_print(f"Assigning connection {connection_id} to parent group {parent_group_id}")
                self.cursor.execute("""
                    UPDATE guacamole_connection
                    SET parent_id = %s
                    WHERE connection_id = %s
                """, (parent_group_id, connection_id))

            self.debug_print(f"Granting permission to {entity_type}:{entity_name}")
            self.cursor.execute("""
                INSERT INTO guacamole_connection_permission (entity_id, connection_id, permission)
                SELECT entity.entity_id, %s, 'READ'
                FROM guacamole_entity entity
                WHERE entity.name = %s AND entity.type = %s
            """, (connection_id, entity_name, entity_type))

        except mysql.connector.Error as e:
            print(f"Error granting connection permission: {e}")
            raise

    def list_users_with_groups(self):
        query = """
            SELECT DISTINCT 
                e1.name as username,
                GROUP_CONCAT(e2.name) as groupnames
            FROM guacamole_entity e1
            JOIN guacamole_user u ON e1.entity_id = u.entity_id
            LEFT JOIN guacamole_user_group_member ugm 
                ON e1.entity_id = ugm.member_entity_id
            LEFT JOIN guacamole_user_group ug
                ON ugm.user_group_id = ug.user_group_id
            LEFT JOIN guacamole_entity e2
                ON ug.entity_id = e2.entity_id
            WHERE e1.type = 'USER'
            GROUP BY e1.name
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        users_groups = {}
        for row in results:
            username = row[0]
            groupnames = row[1].split(',') if row[1] else []
            users_groups[username] = groupnames
        
        return users_groups

    def list_connections_with_groups(self):
        """List all VNC connections with their groups"""
        try:
            self.cursor.execute("""
                SELECT 
                    c.connection_name,
                    MAX(CASE WHEN p1.parameter_name = 'hostname' THEN p1.parameter_value END) AS hostname,
                    MAX(CASE WHEN p2.parameter_name = 'port' THEN p2.parameter_value END) AS port,
                    GROUP_CONCAT(DISTINCT e.name) AS groups
                FROM guacamole_connection c
                LEFT JOIN guacamole_connection_parameter p1 
                    ON c.connection_id = p1.connection_id
                LEFT JOIN guacamole_connection_parameter p2 
                    ON c.connection_id = p2.connection_id
                LEFT JOIN guacamole_connection_permission cp 
                    ON c.connection_id = cp.connection_id
                LEFT JOIN guacamole_entity e 
                    ON cp.entity_id = e.entity_id AND e.type = 'USER_GROUP'
                WHERE c.protocol = 'vnc'
                GROUP BY c.connection_id
                ORDER BY c.connection_name
            """)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error listing connections: {e}")
            raise

    def list_groups_with_users_and_connections(self):
        """List all groups with their users and connections"""
        try:
            # Get users per group
            self.cursor.execute("""
                SELECT 
                    e.name as groupname,
                    GROUP_CONCAT(DISTINCT ue.name) as users
                FROM guacamole_entity e
                LEFT JOIN guacamole_user_group ug ON e.entity_id = ug.entity_id
                LEFT JOIN guacamole_user_group_member ugm ON ug.user_group_id = ugm.user_group_id
                LEFT JOIN guacamole_entity ue ON ugm.member_entity_id = ue.entity_id AND ue.type = 'USER'
                WHERE e.type = 'USER_GROUP'
                GROUP BY e.name
            """)
            groups_users = {row[0]: row[1].split(',') if row[1] else [] for row in self.cursor.fetchall()}

            # Get connections per group
            self.cursor.execute("""
                SELECT 
                    e.name as groupname,
                    GROUP_CONCAT(DISTINCT c.connection_name) as connections
                FROM guacamole_entity e
                LEFT JOIN guacamole_connection_permission cp ON e.entity_id = cp.entity_id
                LEFT JOIN guacamole_connection c ON cp.connection_id = c.connection_id
                WHERE e.type = 'USER_GROUP'
                GROUP BY e.name
            """)
            groups_connections = {row[0]: row[1].split(',') if row[1] else [] for row in self.cursor.fetchall()}

            # Combine results
            result = {}
            for group in set(groups_users.keys()).union(groups_connections.keys()):
                result[group] = {
                    'users': groups_users.get(group, []),
                    'connections': groups_connections.get(group, [])
                }
            return result
        except mysql.connector.Error as e:
            print(f"Error listing groups: {e}")
            raise

    def list_groups_with_users(self):
        query = """
            SELECT 
                e.name as groupname,
                GROUP_CONCAT(DISTINCT ue.name) as usernames
            FROM guacamole_entity e
            LEFT JOIN guacamole_user_group ug ON e.entity_id = ug.entity_id
            LEFT JOIN guacamole_user_group_member ugm ON ug.user_group_id = ugm.user_group_id
            LEFT JOIN guacamole_entity ue ON ugm.member_entity_id = ue.entity_id AND ue.type = 'USER'
            WHERE e.type = 'USER_GROUP'
            GROUP BY e.name
            ORDER BY e.name
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        groups_users = {}
        for row in results:
            groupname = row[0]
            usernames = row[1].split(',') if row[1] else []
            groups_users[groupname] = usernames
        
        return groups_users
