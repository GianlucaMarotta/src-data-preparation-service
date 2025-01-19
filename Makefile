deploy: 
	kubectl create namespace gm-src
	kubectl apply -f k8s_files/local_storage_volume.yaml -n gm-src
	kubectl apply -f k8s_files/user_areas_volume.yaml -n gm-src
	kubectl apply -f k8s_files/prepare-data.yaml -n gm-src
	kubectl apply -f k8s_files/fastapi-service.yaml	-n gm-src
	kubectl apply -f k8s_files/client-pod.yaml -n gm-src

delete:
	kubectl delete namespace gm-src 
	kubectl delete pv local-storage-pv user-areas-pv
