from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields, reqparse
from analyze import read_image

app = Flask(__name__, template_folder='templates')
api = Api(app, version='1.0', title='MLiP-Lab1', description='API for Lab1', 
          doc='/api/docs', prefix='/api/v1')

analysis_ns = api.namespace('analysis', description='Image analysis operations')

parser = reqparse.RequestParser()
parser.add_argument('uri', type=str, required=True, help='Image URI is required', 
                    location='json')

input_model = api.model('AnalysisInput', {
    'uri': fields.String(required=True, description='Image URI to analyze')
})

success_model = api.model('AnalysisSuccess', {
    'text': fields.String(description='Extracted text from image')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@analysis_ns.route("/")
class Analysis(Resource):
    @api.doc('analyze_image', description='Extract text from an image given its URI')
    @api.expect(input_model, validate=True)
    @api.response(200, 'Success', success_model)
    @api.response(400, 'Invalid input', error_model)
    @api.response(500, 'Processing error', error_model)
    def post(self):

        args = parser.parse_args()
        image_uri = args['uri']

        try:
            res = read_image(image_uri)
            return {"text": res}, 200
        except:
            return {'error': 'Error in processing'}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)