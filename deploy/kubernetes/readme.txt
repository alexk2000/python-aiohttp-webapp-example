kubectl get all -l app=app1

psql -h kmaster -p 31875 -U postgres

kubectl create configmap app1-db-dump --from-file=db/web1.sql
