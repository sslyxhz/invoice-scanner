pyinstaller --onefile ^
    --add-data "C:\tools\Miniconda3\envs\invoice\Lib\site-packages\rapidocr_onnxruntime\config.yaml;rapidocr_onnxruntime" ^
    --add-data "C:\tools\Miniconda3\envs\invoice\Lib\site-packages\rapidocr_onnxruntime\models;rapidocr_onnxruntime\models" ^
    main.py