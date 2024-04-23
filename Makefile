transfer_images:
	echo "transferring ./images to trainer/flask/images and resizing them"
	rm -rf ./trainer/flask/images && rm -rf ./trainser/flask/images-resized
	cp -r ./images ./trainer/flask/
	cd ./trainer/flask/ && python3 resize.py
