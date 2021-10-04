from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.helpers.check_user_slovnik import check_user_slovnik_or_create
from website.helpers.pairser import  pairse_cj_x_and_insert, vyhodnot
from website.models.slovicko import Slovicko
from website.models.set_slovicek import SetSlovicek
from website.models.uceni_manager import UceniManager
from website.models.zkouseni_manager import ZkouseniManager
from website.helpers import db_handling



slovnik_views = Blueprint("slovnik_views",__name__)

@slovnik_views.route("/")
@login_required
def restaurant_na_konci_slovniku():
	return redirect(url_for("slovnik_views.slovnik_home"))

@slovnik_views.route("/slovnik_home")
@login_required
def slovnik_home():
	check_user_slovnik_or_create(current_user)
	return render_template("slovnik_home.html")



@slovnik_views.route("/pridej_cjx/<string:jazyk>", methods=["GET", "POST"])
@login_required
def pridej_cjx(jazyk):
    if request.method == "GET":
        return render_template("pridej_cjx.html", jazyk=jazyk)
    if request.method == "POST":
        inpt = request.form.get("input")
        if inpt == "":
            flash("nic jste nezadali")
        else:
            output_pairseru = pairse_cj_x_and_insert(request.form.get("input"),
                                                     jazyk=jazyk,
                                                     asociace=request.form.get("asociace"),
                                                     druh=request.form.get("druh"),
                                                     kategorie=request.form.get("kategorie"),
                                                     obratit=request.form.get("jsem_hloupej"))
            if output_pairseru:
                return render_template("returned_text.html", line=output_pairseru[0], text=output_pairseru[1])

            flash("pridano!", category="info")
        return redirect(url_for("slovnik_views.slovnik_home"))



@slovnik_views.route("/slovnik", methods=["GET", "POST"])
@login_required
def slovnik():
    if request.method == "GET":
        return render_template("slovnik.html", data=Slovicko.get_all())
    if request.method == "POST":
        return redirect(url_for("slovnik_views.edit", date=request.form.get("edit")))


@slovnik_views.route("/edit/<string:date>", methods=["GET", "POST"])
@login_required
def edit(date):
    if request.method == "GET":
        obj = Slovicko.get_by_timestamp(date=date)
        return render_template("edit_slovicko.html", word=obj)
    elif request.method == "POST":
        if request.form.get("potvrdit"):
            old_slovicko = Slovicko.get_by_timestamp(date=date)
            new_obj = Slovicko(czech=request.form.get("czech").split(", "),
                               german=request.form.get("german").split(", "),
                               english=request.form.get("english").split(", "),
                               druh=request.form.get("druh").split(", "),
                               asociace=request.form.get("asociace").split(", "),
                               datum=old_slovicko.datum,
                               times_known=old_slovicko.times_known,
                               times_tested=old_slovicko.times_tested,
                               times_learned=old_slovicko.times_learned,
                               kategorie=request.form.get("kategorie").split(", "))
            new_obj.put_in_db(old_slovicko.datum)
        elif request.form.get("delete"):
            Slovicko.delete_by_timestamp(date)
            flash("smazano slovicko!", category="correct")
        return redirect(url_for("slovnik_views.slovnik"))


@slovnik_views.route("/sort", methods=["GET", "POST"])
@login_required
def sort():
    if request.method == "GET":
        return render_template("sort.html")
    elif request.method == "POST":
        key = request.form.get("only_one_pls")
        sestupne = request.form.get("sestupne")
        db_handling.sort_slovnik(key=key, sestupne=sestupne)
        return redirect(url_for("slovnik_views.slovnik"))


@slovnik_views.route("/singles", methods=["GET", "POST"])
@login_required
def singles():
    if request.method == "GET":
        return render_template("singles.html", singles=Slovicko.get_singles())
    elif request.method == "POST":
        return redirect(url_for("slovnik_views.edit", date=request.form.get("edit")))


@slovnik_views.route("/duplicates", methods=["GET", "POST"])
@login_required
def duplicates():
    if request.method == "GET":
        return render_template("duplicates.html", duplicates=Slovicko.get_duplicates())
    elif request.method == "POST":
        if request.form.get("sjednotit"):
            Slovicko.sjednotit_dve(request.form.get("dat1"), request.form.get("dat2"))
            return redirect(url_for("slovnik_views.duplicates"))
        elif request.form.get("edit"):
            return redirect(url_for("slovnik_views.edit", date=request.form.get("edit")))


@slovnik_views.route("/tvoreni_setu_podle/<string:jazyk>", methods=["GET", "POST"])
@login_required
def tvoreni_setu_podle(jazyk):
    if request.method == "GET":
        s = SetSlovicek()
        s.zapsat_do_souboru()
        return render_template("tvoreni_setu_podle.html")
    elif request.method == "POST":
        typ = request.form.get("typ")
        s = SetSlovicek.nacist_ze_souboru()
        s.podle = typ
        s.jazyk = jazyk
        s.zapsat_do_souboru()
        return redirect(url_for("slovnik_views.tvoreni_setu_meta"))


@slovnik_views.route("/tvoreni_setu_meta/", methods=["GET", "POST"])
@login_required
def tvoreni_setu_meta():
    s = SetSlovicek.nacist_ze_souboru()
    if request.method == "GET":
        return render_template("tvoreni_setu_meta.html",
                               typ=s.podle,
                               kategorie=db_handling.get_kategorie(s.jazyk),
                               druhy=db_handling.get_druhy(s.jazyk))
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
    if len(s.seznam_dat_slovicek) == 0:
        flash("Parametrům neodpovídá ani jedno slovíčko. Zvolte jinak.", category="error")
        return redirect(url_for("slovnik_views.slovnik_home"))
    else:
        if request.method == "GET":
            return render_template("set_overview.html", setik=s.objekty(), jazyk=s.jazyk)
        elif request.method == "POST":
            if request.form.get("zkouseni"):
                z = ZkouseniManager(seznam_dat_slovicek=s.seznam_dat_slovicek,
                                    jazyk=s.jazyk,
                                    podle=s.podle,
                                    podle_meta=s.podle_meta)
                z.zamichat_slovicka()
                z.zapsat_do_souboru()
                return redirect(url_for("slovnik_views.zkouseni", index=0))
            elif request.form.get("uceni"):
                u = UceniManager(seznam_dat_slovicek=s.seznam_dat_slovicek, 
                                 jazyk=s.jazyk,
                                 podle=s.podle,
                                 podle_meta=s.podle_meta)
                u.zapsat_do_souboru()
                return redirect(url_for("slovnik_views.uceni"))


@slovnik_views.route("/zkouseni/<int:index>", methods=["GET", "POST"])
@login_required
def zkouseni(index):
    z = ZkouseniManager.nacist_ze_souboru()
    word = z.nte_ze_setu(index)
    if request.method == "GET":
        if word is False:
            return redirect(url_for("slovnik_views.konec_zkouseni"))
        else:
            return render_template("zkouseni.html", word=word)
    elif request.method == "POST":
        if request.form.get("next"):
            odpoved = request.form.get("pokus")
            z.seznam_odpovedi.append(odpoved)
            vysledek = vyhodnot(jazyk=z.jazyk, predloha=word, string=odpoved)
            if vysledek:
                word.times_tested += 1
                word.times_known += 1
                word.put_in_db(word.datum)
                flash("spravne!", category="correct")
            else:
                word.times_tested += 1
                word.put_in_db(word.datum)
                co_je_dobre = word.pretty(z.jazyk)
                flash(f"spatne, spravne je {co_je_dobre}", category="error")
            z.zapsat_do_souboru()
            return redirect(url_for("slovnik_views.zkouseni", index=index+1))
        elif request.form.get("odevzdat"):
            for i in range(index, len(z.seznam_dat_slovicek)):
                z.seznam_odpovedi.append("skipped")
            z.zapsat_do_souboru()
            return redirect(url_for("slovnik_views.konec_zkouseni"))


@slovnik_views.route("/konec_zkouseni", methods=["GET", "POST"])
@login_required
def konec_zkouseni():
    z = ZkouseniManager.nacist_ze_souboru()
    if request.method == "GET":
        return render_template("konec_zkouseni.html",
                               zkouseni=z,
                               indexes=range(len(z.seznam_dat_slovicek)),
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
            return render_template("uceni.html", display_info=data, typ=typ, jazyk=u.jazyk)
        else:
            return redirect(url_for("slovnik_views.konec_uceni"))
    elif request.method == "POST":
        if request.form.get("dalsi"):
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("vybrat"):
            message, category = u.check_choose(request.form.get("datum_puvodniho"), request.form.get("datum_vybraneho"))
            flash(message,  category=category)
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("zkontrolovat"):
            message, category = u.check_write(request.form.get("datum_puvodniho"), request.form.get("string"))
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
    for zaznam in u.data_o_uceni:
        s = Slovicko.get_by_timestamp(zaznam["datum"])
        s.times_learned += 1
        s.put_in_db(s.datum)
    if request.method == "GET":
        return render_template("konec_uceni.html")
    elif request.method == "POST":
        if request.form.get("retake"):
            u.retake()
            return redirect(url_for("slovnik_views.uceni"))
        elif request.form.get("nove"):
            return redirect(url_for("slovnik_views.slovnik_home"))
        elif request.form.get("vyzkouset"):
            z = ZkouseniManager(jazyk=u.jazyk)
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
            return redirect(url_for("slovnik_views.detail_zkouseni", datum=detail))
        return redirect(url_for("slovnik_views.slovnik_home"))


@slovnik_views.route("/detail/<string:datum>", methods=["GET", "POST"])
@login_required
def detail_zkouseni(datum):
    if request.method == "GET":
        z, message = ZkouseniManager.get_by_timestamp(datum)
        if message == "":
            pass
        else:
            flash(message, category="info")
        return render_template("detail_zkouseni.html",
                               zkouseni=z,
                               zkousena_slovicka=z.objekty(),
                               indexy=range(len(z.seznam_dat_slovicek)))
    elif request.method == "POST":
        retake = request.form.get("retake")
        delete = request.form.get("delete")
        if retake:
            ZkouseniManager.znovu(retake)
            return redirect(url_for("slovnik_views.zkouseni", index=0))
        elif delete:
            ZkouseniManager.delete_by_timestamp(datum)
            flash("Záznam o zkoušení smazán.", category="info")
            return redirect(url_for("slovnik_views.historie_zkouseni"))


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
        if request.form.get("all"):
            db_handling.natahnout_od_pipa()
        else:
            db_handling.natahnout_od_pipa(request.form.getlist("kategorie"))
        return redirect(url_for("slovnik_views.slovnik"))




