function move(data) { //always keep dx dy jednotkovy vektor
    let ryby = data["ryby"]
    let v = data["v"]
    let width = data["width"]
    let height = data["height"]
    let sirka_zony = data["sirka_zony"]
    let koef_od_kraju = data["koef_od_kraju"]
    let koef_odpuzovaci = data["koef_odpuzovaci"]
    let koef_pritahovaci = data["koef_pritahovaci"]
    let polomer_dohledu = data["polomer_dohledu"]
    let osobni_polomer = data["osobni_polomer"]
    let koef_usmernovaci = data["koef_usmernovaci"]
    let prostor_usmernovani = data["prostor_usmernovani"]
    
    for (let i = 0; i < ryby.length; i++) {
        let prvniRyba = ryby[i]
        let od_kraju_vektor = [0,0]
        let odpuzovaci_vektor = [0,0]
        let pritahovaci_vektor = [0,0]
        let usmernovaci_vektor = [0,0]
        let temp_koef = 0;
        for (let j = 0; j < ryby.length; j++) {
            let druhaRyba = ryby[j]
            if (prvniRyba.id != druhaRyba.id) {
                let vzdalenost = vzdalenost_r1r2(prvniRyba,druhaRyba)
                
                // pritahovani k sobe
                if (vzdalenost < polomer_dohledu) {
                    let vektor_k_ni = vektor_na_jednotkovy(vektor_r1r2(prvniRyba,druhaRyba))
                    pritahovaci_vektor[0] += vektor_k_ni[0]
                    pritahovaci_vektor[1] += vektor_k_ni[1]
                }
                
                //usmernovani
                if (vzdalenost < prostor_usmernovani) {
                    usmernovaci_vektor[0] += druhaRyba.dx-prvniRyba.dx
                    usmernovaci_vektor[1] += druhaRyba.dy-prvniRyba.dy
                }
                
                //odpuzovani od sebe
                // fce y = c*((R-x)/Rx) je klicova k tomu udrzovani vzdalenosti
                if (vzdalenost < osobni_polomer) {
                    temp_koef = koef_odpuzovaci*((osobni_polomer - vzdalenost)/(osobni_polomer*vzdalenost))
                    let vektor_od_ni = vektor_na_jednotkovy(vektor_r1r2(druhaRyba,prvniRyba))
                    odpuzovaci_vektor[0] += vektor_od_ni[0]*temp_koef
                    odpuzovaci_vektor[1] += vektor_od_ni[1]*temp_koef
                } 
            }
        }
        //odpuzovani od kraju
        if (prvniRyba.x > width-sirka_zony) {
            od_kraju_vektor[0] = -1
        }
        if (prvniRyba.x < sirka_zony) {
            od_kraju_vektor[0] = 1
        }
        if (prvniRyba.y > height-sirka_zony) {
            od_kraju_vektor[1] = -1
        } 
        if (prvniRyba.y < sirka_zony) {
            od_kraju_vektor[1] = 1
        }
        od_kraju_vektor = vektor_na_jednotkovy(od_kraju_vektor) // v pripade rohu by jeho velikost byla sqrt(2)


        //tady se pridavaj vlivy
        prvniRyba.novedx += (od_kraju_vektor[0]*koef_od_kraju + odpuzovaci_vektor[0]*koef_odpuzovaci + pritahovaci_vektor[0]*koef_pritahovaci + usmernovaci_vektor[0]*koef_usmernovaci)
        prvniRyba.novedy += (od_kraju_vektor[1]*koef_od_kraju + odpuzovaci_vektor[1]*koef_odpuzovaci + pritahovaci_vektor[1]*koef_pritahovaci + usmernovaci_vektor[1]*koef_usmernovaci)


        //tady se forcuje smerovy vektor na 0.3 < |v| < 1
        let min_velikost_smer_vektoru = 0.7
        let max_velikost_smer_vektoru = 2
        let velikost_smeroveho_vektoru = velikost_vektoru([prvniRyba.novedx, prvniRyba.novedy])
        if (velikost_smeroveho_vektoru > max_velikost_smer_vektoru) {
            let jednotkovy = vektor_na_jednotkovy([prvniRyba.novedx, prvniRyba.novedy])
            prvniRyba.novedx= jednotkovy[0]
            prvniRyba.novedy= jednotkovy[1]
        }
        if (velikost_smeroveho_vektoru < min_velikost_smer_vektoru) {
            let k = Math.sqrt((min_velikost_smer_vektoru**2)/(prvniRyba.novedx**2 + prvniRyba.novedy**2))
            prvniRyba.novedx *= k
            prvniRyba.novedy *= k
        }


        //tady se hejbe s rybou
        prvniRyba.novex += prvniRyba.novedx*v
        prvniRyba.novey += prvniRyba.novedy*v
    }
    
    //prepsani novych xy na akual xy
    for (let i=0; i<ryby.length; i++)  {
        ryby[i].x = ryby[i].novex
        ryby[i].y = ryby[i].novey
        ryby[i].dx = ryby[i].novedx
        ryby[i].dy = ryby[i].novedy
    }

    return ryby
}



function vzdalenost_r1r2(ryba1, ryba2)  {
    return Math.sqrt((ryba2.x - ryba1.x)**2 + (ryba2.y - ryba1.y)**2)
}


function vektor_r1r2(ryba1, ryba2) {
    return [ryba2.x-ryba1.x, ryba2.y-ryba1.y]
}


function vektor_na_jednotkovy(vektor) {
    let velikost = velikost_vektoru(vektor)
    if (velikost == 0) {
        return [0,0]
    } else {
        return [vektor[0]/velikost, vektor[1]/velikost]
    }
}


function velikost_vektoru(vektor) {
    return Math.sqrt(vektor[0]**2 + vektor[1]**2)
}

export {move}