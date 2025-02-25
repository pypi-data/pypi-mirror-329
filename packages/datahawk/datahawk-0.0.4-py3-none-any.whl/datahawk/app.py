import os
from argparse import ArgumentParser

from flask import Flask, render_template, request

from datahawk.datahawk import Datahawk

app = Flask(__name__)
datahawk = None


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    global data_inspector
    cache_dir = app.config.get("CACHE_DIR", None)
    if request.method == "POST":
        try:
            data_path = request.form.get("data_path", None).strip()
            read_mode = request.form.get("read_mode", None)
            source = request.form.get("source", None)
            split = request.form.get("split", None).strip()
            config_name = request.form.get("config_name", None).strip()
            # create a new instance of Datahawk
            data_inspector = Datahawk(
                data_path, read_mode, source, 
                split=split, config_name=config_name,
                cache_dir=cache_dir
            )
            return data_inspector.render()
        except (RuntimeError, FileNotFoundError) as e:
            return render_template(
                "index.html", 
                error_message="ERROR: " + str(e)
            )
        except:
            raise
    return render_template("index.html")


@app.route("/update_index", methods=["POST"])
def user_update_index() -> str:
    """"""
    global data_inspector
    new_index = request.form.get("indexInput", None).strip()
    return data_inspector.user_update_index(new_index)


@app.route("/random_json")
def random_json() -> str:
    """"""
    global data_inspector
    return data_inspector.random_json()


@app.route("/first_item")
def first_item() -> str:
    """"""
    global data_inspector
    return data_inspector.first_item()


@app.route("/previous_item")
def previous_item() -> str:
    """"""
    global data_inspector
    return data_inspector.previous_item()


@app.route("/next_item")
def next_item() -> str:
    """"""
    global data_inspector
    return data_inspector.next_item()


@app.route("/last_item")
def last_item() -> str:
    """"""
    global data_inspector
    return data_inspector.last_item()


@app.route("/filter_data", methods=["POST"])
def filter_data() -> str:
    """"""
    global data_inspector
    # get the filters
    filter_list = []
    for key in request.form:
        if key.startswith("filter_"):
            filter_list.append(request.form[key])
    return data_inspector.filter_data(filter_list)


@app.route("/sort_data", methods=["POST"])
def sort_data() -> str:
    """"""
    global data_inspector
    # get the sorting keys
    key_list = []
    for key in request.form:
        if key.startswith("key_"):
            key_list.append(request.form[key])
    return data_inspector.sort_data(key_list)


def main():
    # parse args
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5009,
                        help="Port number to run the app on. Default is 5009.")
    parser.add_argument("--cache_dir", type=str, 
                        default=os.path.join(os.path.expanduser("~"), ".cache/datahawk/"),
                        help="Cache directory to store temporary data files")
    args = parser.parse_args()
    
    # cache dir for the app run
    if not os.path.exists(args.cache_dir):
        os.makedirs(args.cache_dir)
    app.config["CACHE_DIR"] = args.cache_dir

    # run the app
    app.run(port=args.port)


if __name__ == "__main__":
    main()
