SET ECHO OFF
echo 'converting documents into images...'
python .\process-document.py
echo 'finished'

echo 'processing images into text...'
python .\process-images.py
echo 'finished'
echo 'classifying text...'
python .\classify-document.py >> classfication.md
echo 'finished'
