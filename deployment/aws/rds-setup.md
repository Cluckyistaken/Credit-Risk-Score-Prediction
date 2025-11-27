# RDS (Postgres) Setup (manual guidance)

1. In AWS console -> RDS -> Create database
   - Engine: PostgreSQL (version 15 recommended)
   - Templates: Production or Dev/test (choose as needed)
   - DB instance size: db.t3.medium (or as required)
   - Storage: General Purpose (gp3) 20GB+
2. Network & Security:
   - Place DB in private subnets of your VPC.
   - Create or attach a Security Group allowing port 5432 from your app subnet / security group only.
3. Credentials:
   - Choose master username and strong password; store in Secrets Manager.
4. Backups:
   - Enable automated backups, set retention (e.g., 7 days).
   - Enable Multi-AZ for high availability if needed.
5. Monitoring:
   - Enable enhanced monitoring and CloudWatch alarms for CPU, storage, connections.
6. Connect:
   - Use the RDS endpoint and credentials in your backend config (via Secrets Manager or environment variables).
   - Example connection string:
     ```
     postgres://<user>:<password>@<rds-endpoint>:5432/<dbname>
     ```
7. Migrations:
   - Run DB migrations from CI/CD or during deployment using a migration tool (Flyway, Alembic, Knex, Liquibase).
