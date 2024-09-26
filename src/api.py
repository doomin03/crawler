from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_cors import CORS
from modules.CGV import main_view, movie_list


app = Flask(__name__)
api = Api(app, title="CGV API", description="CGV 영화 정보를 제공하는 API입니다.")
CORS(app)

ns_cgv = api.namespace('cgv', description='CGV 영화 정보 API')


@ns_cgv.route('/main-view')
class CGVMainView(Resource):
    def get(self):
        try:

            data = main_view().data
            return jsonify(data)
        except Exception as e:
            return {"error": str(e)}, 500


@ns_cgv.route('/movie-list')
class CGVMovieList(Resource):
    def get(self):
        try:

            movie_data = movie_list().data_list
            return jsonify(movie_data)
        except Exception as e:
            return {"error": str(e)}, 500


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
