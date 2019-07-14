import coremltools

coreml_model = coremltools.converters.keras.convert(
    'vgg16_transfer.h5',
    input_names='image',
    image_input_names='image',
    output_names='Prediction',
    class_labels=['apple', 'tomato', 'strawberry'],
    )

coreml_model.save('./vgg16_transfer.mlmodel')
