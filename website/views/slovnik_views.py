from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from website.helpers.pairser import  pairse_and_insert, vyhodnot
from website.models.slovicko import Slovicko
from website.models.set_slovicek import SetSlovicek
from website.models.uceni_manager import UceniManager
from website.models.zkouseni_manager import ZkouseniManager
from website.models.slovnik import Slovnik
from website.json_handlers import db_handling
from website.models.settings import Settings
import json



slovnik_views = Blueprint("slovnik_views",__name__)

@slovnik_views.route("/")
@login_required
def restaurant_na_konci_slovniku():
	return redirect(url_for("slovnik_views.slovnik_home"))

@slovnik_views.route("/slovnik_home")
@login_required
def slovnik_home():
    return render_template("slovnik_home.html")



@slovnik_views.route("/pridej_slovicka", methods=["GET", "POST"])
@login_required
def pridej_slovicka():
    settings = Settings.get()
    if request.method == "GET":
        return render_template("pridej_slovicka.html", jazyky = json.dumps(settings.data["jazyky"]))
    if request.method == "POST":
        inpt = request.form.get("input")
        if inpt == "":
            flash("nic jste nezadali",category="info")
        else:
            output_pairseru = pairse_and_insert(request.form.get("input"),
                                                jazyky = request.form.getlist("dropdown_jazyka"),
                                                asociace=request.form.get("asociace"),
                                                druh=request.form.get("druh"),
                                                kategorie=request.form.get("kategorie"))
            if output_pairseru:
                return render_template("returned_text.html", line=output_pairseru[0], text=output_pairseru[1])

            flash("pridano!", category="info")
        return redirect(url_for("slovnik_views.slovnik_home"))



@slovnik_views.route("/slovnik", methods=["GET", "POST"])
@login_required
def slovnik():
    if request.method == "GET":
        s = Slovnik.get()
        return render_template("slovnik.html", slovicka = s.slovicka, jazyky = Settings.get().data["jazyky"])
    if request.method == "POST":
        if request.form.get("dropdown_trigger"):
            seznam_id = request.form.getlist("checked")
            dropdown_moznost = request.form.get("dropdown")
            dropdown_meta = request.form.get("dropdown_meta")
            print(seznam_id, dropdown_meta, dropdown_moznost)
            return f"Not implemented yet, ale id jsou:" + ", ".join(seznam_id)
        elif request.form.get("edit"):
            return redirect(url_for("slovnik_views.edit", id=request.form.get("edit")))


@slovnik_views.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id: int):
    if request.method == "GET":
        slovicko = json.dumps(db_handling.get_by_id(id))
        jazyky = json.dumps(Settings.get().data["jazyky"])
        return render_template("edit_slovicko.html", slovicko=slovicko, jazyky=jazyky)
    elif request.method == "POST":
        if request.form.get("potvrdit"):
            new_data = json.loads(request.form.get("slovicko"))
            db_handling.delete_by_id(int(new_data["id"]))
            db_handling.insert_to_db(new_data)
        elif request.form.get("delete"):
            db_handling.delete_by_id(id=id)
            flash("smazano slovicko!", category="succcess")
        return redirect(url_for("slovnik_views.slovnik"))
        


@slovnik_views.route("/sort", methods=["GET", "POST"])
@login_required
def sort():
    if request.method == "GET":
        return render_template("sort.html")
    elif request.method == "POST":
        key = request.form.get("only_one_pls")
        sestupne = request.form.get("sestupne")  # Vraci "True" nebo None
        if sestupne == "True":
            sestupne = True
        else:
            sestupne = False
        db_handling.sort_slovnik(key=key, sestupne=sestupne)
        return redirect(url_for("slovnik_views.slovnik"))


@slovnik_views.route("/singles", methods=["GET", "POST"])
@login_required
def singles():
    if request.method == "GET":
        return render_template("singles.html", singles=Slovicko.get_singles())
    elif request.method == "POST":
        return redirect(url_for("slovnik_views.edit", id=request.form.get("edit")))


@slovnik_views.route("/duplicates", methods=["GET", "POST"])
@login_required
def duplicates():
    s = Slovnik.get()
    if request.method == "GET":
        duplicates = s.get_duplicates()
        return render_template("duplicates.html", duplicates=duplicates)
    elif request.method == "POST":
        if request.form.get("sjednotit"):
            s.sjednotit(request.form.getlist("id"))
            return redirect(url_for("slovnik_views.duplicates"))
        elif request.form.get("edit"):
            return redirect(url_for("slovnik_views.edit", id=request.form.get("edit")))



@slovnik_views.route("/tvoreni_setu_podle", methods=["GET", "POST"])
@login_required
def tvoreni_setu_podle():
    if request.method == "GET":
        s = SetSlovicek()
        s.zapsat_do_souboru()
        jazyky = Settings.get().data["jazyky"]
        return render_template("tvoreni_setu_podle.html", jazyky = json.dumps(jazyky))
    elif request.method == "POST":
        s = SetSlovicek.nacist_ze_souboru()
        s.podle = request.form.get("typ")
        s.base_jazyk = request.form.get("base_jazyk")
        s.target_jazyk = request.form.get("target_jazyk")
        s.zapsat_do_souboru()
        return redirect(url_for("slovnik_views.tvoreni_setu_meta"))


@slovnik_views.route("/tvoreni_setu_meta/", methods=["GET", "POST"])
@login_required
def tvoreni_setu_meta():
    s = SetSlovicek.nacist_ze_souboru()
    if request.method == "GET":
        return render_template("tvoreni_setu_meta.html",
                               typ=s.podle,
                               kategorie=db_handling.get_kategorie(base_jazyk = s.base_jazyk, target_jazyk = s.target_jazyk),
                               druhy=db_handling.get_druhy(base_jazyk = s.base_jazyk, target_jazyk = s.target_jazyk))
    elif request.method == "POST":
        if s.podle == "datum":
            s.pripravit_set_od_do(request.form.get("od"), request.form.get("do"))
        elif s.podle == "kategorie":
            s.pripravit_set_kategorie(request.form.get("kategorie"))
        elif s.podle == "neuspesne":
            s.pripravit_set_neuspesnych(int(request.form.get("neuspesne")))
        elif s.podle == "vse":
            s.pripravit_set_vse(int(request.form.get("vse")))
        elif s.podle == "least":
            s.pripravit_set_least(int(request.form.get("least")))
        elif s.podle == "druh":
            s.pripravit_set_druhy(request.form.get("druhy"))
        elif s.podle == "skupina":
            s.pripravit_set_skupina(request.form.get("skupina"))
        elif s.podle == "nejmene_ucene":
            s.pripravit_set_nejmene_ucene(int(request.form.get("nejmene_ucene")))
        else:
            return "not implemented yet"
        return redirect(url_for("slovnik_views.set_overview"))


@slovnik_views.route("/set_overview", methods=["GET", "POST"])
@login_required
def set_overview():
    s = SetSlovicek.nacist_ze_souboru()
    if len(s.seznam_id_slovicek) == 0:
        flash("Parametrům neodpovídá ani jedno slovíčko. Zvolte jinak.", category="error")
        return redirect(url_for("slovnik_views.slovnik_home"))
    else:
        if request.method == "GET":
            return render_template("set_overview.html", setik=s.objekty(), target_jazyk=s.target_jazyk, base_jazyk = s.base_jazyk)
        elif request.method == "POST":
            if request.form.get("zkouseni"):
                z = ZkouseniManager(seznam_id_slovicek=s.seznam_id_slovicek,
                                    target_jazyk=s.target_jazyk,
                                    base_jazyk=s.base_jazyk,
                                    podle=s.podle,
                                    podle_meta=s.podle_meta)
                z.zamichat_slovicka()
                z.zapsat_do_souboru()
                return redirect(url_for("slovnik_views.zkouseni", index=0))
            elif request.form.get("uceni"):
                u = UceniManager(seznam_id_slovicek=s.seznam_id_slovicek, 
                                 target_jazyk=s.target_jazyk,
                                 base_jazyk=s.base_jazyk,
                                 podle=s.podle,
                                 podle_meta=s.podle_meta)
                u.zapsat_do_souboru()
                return redirect(url_for("slovnik_views.uceni"))


@slovnik_views.route("/zkouseni/<int:index>", methods=["GET", "POST"])
@login_required
def zkouseni(index: int):
    z = ZkouseniManager.nacist_ze_souboru()
    word = z.nte_ze_setu(index)
    if request.method == "GET":
        if word is False:
            return redirect(url_for("slovnik_views.konec_zkouseni"))
        else:
            return render_template("zkouseni.html", word=word, index=index, celkem = len(z.seznam_id_slovicek), target_jazyk=z.target_jazyk, base_jazyk = z.base_jazyk)
    elif request.method == "POST":
        if request.form.get("next"):
            odpoved = request.form.get("pokus")
            z.seznam_odpovedi.append(odpoved)
            vysledek = vyhodnot(jazyk=z.target_jazyk, predloha=word, string=odpoved)
            if vysledek:
                word.times_tested += 1
                word.times_known += 1
                word.put_in_db()
                flash("spravne!", category="success")
            else:
                word.times_tested += 1
                word.put_in_db()
                co_je_dobre = word.pretty(z.target_jazyk)
                flash(f"spatne, spravne je {co_je_dobre}", category="error")
            z.zapsat_do_souboru()
            return redirect(url_for("slovnik_views.zkouseni", index=index+1))
        elif request.form.get("odevzdat"):
            for i in range(index, len(z.seznam_id_slovicek)):
                z.seznam_odpovedi.append("skipped")
            z.zapsat_do_souboru()
            return redirect(url_for("slovnik_views.konec_zkouseni"))


@slovnik_views.route("/konec_zkouseni", methods=["GET", "POST"])
@login_required
def konec_zkouseni():
    z = ZkouseniManager.nacist_ze_souboru()
    z.uspesnost = z.get_uspesnost()
    if request.method == "GET":
        return render_template("konec_zkouseni.html",
                               zkouseni=z,
                               indexes=range(len(z.seznam_id_slovicek)),
                               zkousena_slovicka=z.objekty(),
                               seznam_yesno=z.get_seznam_yesno())
    elif request.method == "POST":
        z.poznamka = request.form.get("poznamka")
        z.zapsat_do_souboru()
        z.ulozit_do_historie()
        return redirect(url_for("slovnik_views.slovnik_home"))


@slovnik_views.route("/uceni/", methods=["GET", "POST"])
@login_required
def uceni():
    u = UceniManager.nacist_ze_souboru()
    if request.method == "GET":
        next_display_info = u.get_next_data()
        if next_display_info:
            typ, data = next_display_info
            return render_template("uceni.html", display_info=data, typ=typ, target_jazyk=u.target_jazyk, base_jazyk = u.base_jazyk ,pocet_written = u.get_pocet_written())
        else:
            return redirect(url_for("slovnik_views.konec_uceni"))
    elif request.method == "POST":
        if request.form.get("dalsi"):
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("vybrat"):
            message, category = u.check_choose(id_puvodniho=int(request.form.get("id_puvodniho")), id_vybraneho=int(request.form.get("id_vybraneho")))
            flash(message,  category=category)
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("zkontrolovat"):
            message, category = u.check_write(id=int(request.form.get("id_puvodniho")), string=request.form.get("string"))
            flash(message,category=category)
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("ukoncit"):
            return redirect(url_for("slovnik_views.konec_uceni"))
        else:
            return "Zaboha nevim jak jsem se sem dostal"


@slovnik_views.route("/konec_uceni", methods=["GET", "POST"])
@login_required
def konec_uceni():
    u = UceniManager.nacist_ze_souboru()
    if request.method == "GET":
        for zaznam in u.data_o_uceni:
            s = Slovicko.get_by_id(zaznam["id"])
            s.times_learned += 1
            s.put_in_db()
        return render_template("konec_uceni.html")
    elif request.method == "POST":
        if request.form.get("retake"):
            u.retake()
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("nove"):
            return redirect(url_for("slovnik_views.slovnik_home"))
        elif request.form.get("vyzkouset"):
            z = ZkouseniManager(target_jazyk=u.target_jazyk, base_jazyk=u.base_jazyk)
            z.nacist_z_dat_o_uceni(data_o_uceni=u.data_o_uceni, podle=u.podle, podle_meta=u.podle_meta)
            return redirect(url_for("slovnik_views.zkouseni", index=0))


@slovnik_views.route("/historie_zkouseni", methods=["GET", "POST"])
@login_required
def historie_zkouseni():
    if request.method == "GET":
        return render_template("historie_zkouseni.html", historie=ZkouseniManager.get_all_from_history())
    elif request.method == "POST":
        detail = request.form.get("detail")
        if detail:
            return redirect(url_for("slovnik_views.detail_zkouseni", id=int(detail)))
        return redirect(url_for("slovnik_views.slovnik_home"))


@slovnik_views.route("/detail/<int:id>", methods=["GET", "POST"])
@login_required
def detail_zkouseni(id):
    if request.method == "GET":
        z = ZkouseniManager.get_by_id(id)
        objekty = z.objekty()
        return render_template("detail_zkouseni.html",
                               zkouseni=z,
                               zkousena_slovicka=objekty,
                               indexy=range(len(objekty)))
    elif request.method == "POST":
        retake = request.form.get("retake")
        delete = request.form.get("delete")
        edit = request.form.get("edit")
        if retake:
            ZkouseniManager.znovu(int(retake))
            return redirect(url_for("slovnik_views.zkouseni", index=0))
        elif delete:
            ZkouseniManager.delete_by_id(int(delete))
            flash("Záznam o zkoušení smazán.", category="info")
            return redirect(url_for("slovnik_views.historie_zkouseni"))
        elif edit:
            return redirect(url_for("slovnik_views.edit", id = int(edit)))



@slovnik_views.route("/about")
@login_required
def about():
    return render_template("about.html")


@slovnik_views.route("/prejmenovat_kategorii", methods=["GET","POST"])
@login_required
def prejmenovat_kategorii():
    if request.method == "GET":
        return render_template("prejmenovat_kategorii.html", kategorie = db_handling.get_kategorie())
    else:
        return "Not implemented yet"


@slovnik_views.route("/natahnout_od_pipa", methods=["GET","POST"])
@login_required
def natahnout_od_pipa():
    if request.method == "GET":
        return render_template("natahnout_od_pipa.html", kategorie = db_handling.get_kategorie_od_piipa())
    else:
        s = Slovnik.get()
        if request.form.get("all"):
            s.natahnout_od_pipa()
        else:
            s.natahnout_od_pipa(request.form.getlist("kategorie"))
        return redirect(url_for("slovnik_views.slovnik"))




