# To Do
Take a picture on the iPhone using the model created [last time(vgg16_transfer)](https://github.com/hiraku00/vgg16_transfer) and try to judge it.

# Summary
1. Convert model (.h5) created by Keras
2. Create a project in Xcode
3. Screen part creation & code association
4. Allow access to camera & add code to start camera
5. Behavior when the button (take a photo) is pressed
6. Load the model and judge

# Operating Environment
- macOS Catalina 10.15 beta
- Python 3.6.8
- keras 2.2.4
- coremltools 2.1.0
- Xcode 10.2.1

# 1. Convert model (.h5) created by Keras
-Use the model (vgg16_transfer.h5) created last time and convert it to a model available on iOS

```python:model conversion
import coremltools

coreml_model = coremltools.converters.keras.convert(
    'vgg16_transfer.h5',
    input_names='image',
    image_input_names='image',
    output_names='Prediction',
    class_labels=['apple', 'tomato', 'strawberry'],
    )

coreml_model.save('./vgg16_transfer.mlmodel')
```

# 2. Create a project in Xcode
- Launch Xcode and select "Create a new Xcode project"
<img width="494" alt="1.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/361ef47a-8827-0955-0f2b-8341cb8808ba.png">
- Select "Single View App"
<img width="730" alt="2.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/b642517d-7efe-4a8b-c7bd-dd3db99192c9.png">
- 'Product Name' is an arbitrary name. Language is "Swift", all check boxes (Use XX, include XX) are removed and the Next button is pressed

# 3. Screen part creation & code association
- Add the following 3 screen parts on Xcode
 - Image View(area for displaying photos)
 - Text View(area for displaying judgment results)
 - Button(button to start the camera)

- Make a layout like this
<img width="553" alt="3.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/b327fe7a-0a54-bcb4-dd33-d03f5801d98c.png">

-　Associate each part
-　Add Image View and Text View under "class ViewController" (select parts and add while pressing the control key)
-　Add Button under "override func viewDidLoad()"
-　Set Name and Connection below
 - Image View : imageDisplay(Connection : Outlet)
 - Text View : predictionDisplay(Connection : Outlet)
 - Button : takePhoto(Connection : Action)

```swift:association of each part
    # Image View
    @IBOutlet weak var imageDisplay: UIImageView!
    # Text View
    @IBOutlet weak var predictionDisplay: UITextView!
    # Button
    @IBAction func takePhoto(_ sender: Any) {
    }
```

# 4. Allow access to camera & add code to start camera
- Add "Privacy-Camera Usage Description" to info.plist and allow access to the camera
<img width="842" alt="４.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/4beff109-742e-82f8-e020-e117170714c6.png">

- Add the following two "delegate"(event detection and processing).(Screen to display the camera, it is possible to return to the original screen when you save the photo)
 - UIImagePickerControllerDelegate
 - UINavigationControllerDelegate
- Added variable "imagePicker" to display the screen for taking a picture
- Add code to initialize "imagePicker" immediately after the app starts up in "viewDidLoad()"


```swift:start camera(before)
class ViewController: UIViewController {

    @IBOutlet weak var imageDisplay: UIImageView!
    @IBOutlet weak var predictionDisplay: UITextView!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    # ~~~ Omission ~~~
}
```

```swift:start camera(after)
class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var imageDisplay: UIImageView!
    @IBOutlet weak var predictionDisplay: UITextView!
    var imagePicker: UIImagePickerController!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        # initialize
        imagePicker = UIImagePickerController()
        # delegate:Variable to pass event
        imagePicker.delegate = self
        # sourceType : Take data from camera or read from album -> 'camera' this time
        imagePicker.sourceType = .camera
    }

    # ~~~ Omission ~~~
}
```

# 5. Behavior when the button (take a photo) is pressed
- Call the present function with "takePhoto" to display the imagePicker created in '4.'.

```swift:before
    @IBAction func takePhoto(_ sender: Any) {
    }
```
```swift:after
    @IBAction func takePhoto(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }
```

- Describe the process after taking a picture(imagePickerController)
- Update the image attribute of imageDisplay
- Since the taken image is included in info, take it out and set it to the image attribute of imageDisplay
- Set properties called "originalImage" because 'UIImagePickerController.InfoKey' of 'info' contains various attributes(specify type with 'as? UIImage')
- Close the previous ImagePicker after setting the image(dismiss)

```swift:after
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        imageDisplay.image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
        imagePicker.dismiss(animated: true, completion: nil)
    }
```

# 6. Load the model and judge
- Load mlmodel and pass an image file to that model to judge
- Drag and drop the model (vgg16_transfer.mlmodel) converted in '1.' into the Xcode project

<img width="730" alt="7.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/f0d1f30f-a7af-3144-1076-0682caac3b0a.png">

<img width="323" alt="8.png" src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/67194/7a64d2ba-a3a9-51ae-7425-48bd0758188a.png">

- Add the following library
 - CoreML : Machine Learning Library
 - Vision : Library for handling image files
 
```swift:add library
import CoreML
import Vision
```

- Add judgment processing
- Add decision processing (imagePrediction) after imagePickerController
- Specify an image file as an argument (the same as the content displayed on the screen (imageDisplay.image))

```swift:before
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        imageDisplay.image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
        imagePicker.dismiss(animated: true, completion: nil)
    }
```

```swift:after
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        imageDisplay.image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
        imagePicker.dismiss(animated: true, completion: nil)
        imagePrediction(image: (info[UIImagePickerController.InfoKey.originalImage] as? UIImage)!)
    }
```

-Create a function of judgment processing(imagePrediction)
-Load model

```swift:load model
    func imagePrediction(image: UIImage) {
        guard let model = try? VNCoreMLModel(for: vgg16_transfer().model) else {
            fatalError("Model not found")
        }
```

- Create an instance of VNCoreMLRequest
- Store the judgement result in results (The judgement result is returned in the variable "VNClassificationObservation")
- High score data is stored in 'results.first'
- Display judgement results on 'predictionDiaplay'
 - firstResult.confidence : Probability(Because it is stored in decimal, multiply by 100 and display as a percentage.)
 - firstResult.identifier : Label (judgement result)

```swift:model judgment processing
        let request = VNCoreMLRequest(model: model) {
            [weak self] request, error in
            
            guard let results = request.results as? [VNClassificationObservation],
                let firstResult = results.first else {
                    fatalError("No results found")
            }
            
            DispatchQueue.main.async {
                self?.predictionDisplay.text = "Accuracy: = \(Int(firstResult.confidence * 100))% \n\nラベル: \((firstResult.identifier))"
            }
        }
```

- requestに対する処理を記載
- ciImageというデータ型に変換できないと推定処理が出来ないため、取得出来ない場合はエラー
- Visionフレームワークで画像を使うためのimageHandlerという変数を宣言し、VNImageRequestHandlerを生成
- imageHandlerにrequestを実行させる

- Describe processing for request
- Error can not be obtained because it can not be determined if conversion can not be performed to the data type 'ciImage'
- Declare "imageHandler" variable for using image in Vision framework and generate "VNImageRequestHandler"
- make 'imageHandler' execute 'request'

```swift
        guard let ciImage = CIImage(image: image) else {
            fatalError("Can't convert image.")
        }
        
        let imageHandler = VNImageRequestHandler(ciImage: ciImage)
        
        DispatchQueue.global(qos: .userInteractive).async {
            do {
                try imageHandler.perform([request])
            } catch {
                print("Error")
            }
        }
```

- The whole code is as follows

```swift:ViewController.swift
import UIKit
import CoreML
import Vision

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var imageDisplay: UIImageView!
    @IBOutlet weak var predictionDisplay: UITextView!
    var imagePicker: UIImagePickerController!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        imagePicker = UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .camera
    }
    @IBAction func takePhoto(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        imageDisplay.image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
        imagePicker.dismiss(animated: true, completion: nil)
        imagePrediction(image: (info[UIImagePickerController.InfoKey.originalImage] as? UIImage)!)
    }
    
    func imagePrediction(image: UIImage) {
        guard let model = try? VNCoreMLModel(for: vgg16_transfer().model) else {
            fatalError("Model not found")
        }
        
        let request = VNCoreMLRequest(model: model) {
            [weak self] request, error in
            
            guard let results = request.results as? [VNClassificationObservation],
                let firstResult = results.first else {
                    fatalError("No results found")
            }
            
            DispatchQueue.main.async {
                self?.predictionDisplay.text = "Accuracy: = \(Int(firstResult.confidence * 100))% \n\nラベル: \((firstResult.identifier))"
            }
        }
        
        guard let ciImage = CIImage(image: image) else {
            fatalError("Can't convert image.")
        }
        
        let imageHandler = VNImageRequestHandler(ciImage: ciImage)
        
        DispatchQueue.global(qos: .userInteractive).async {
            do {
                try imageHandler.perform([request])
            } catch {
                print("Error")
            }
        }
    }
}
```

# References
- [Classifying Images with Vision and Core ML](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml)

# in Japanese
- [Qiita(Kerasで作成したモデルを変換してiOSに組み込み)](https://qiita.com/hiraku00/items/bc95717e3d154d6243f5)
