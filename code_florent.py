Sub Geocoding()
    Dim Address As Object
    Dim scriptControl As Object

    Set scriptControl = CreateObject("MSScriptControl.ScriptControl")
    scriptControl.Language = "JScript"
    scriptControl.AddCode "function getLocality(jsonObj) { if(jsonObj.results[0] === undefined) return -1; var compo = jsonObj.results[0].address_components; for (var i = 0; i < compo.length; i++) {for (var j = 0; j < compo[i].types.length; j++) { if (compo[i].types[j] == 'locality') {return compo[i].long_name;} } } }"
    scriptControl.AddCode "function getRegion(jsonObj) { if(jsonObj.results[0] === undefined) return -1; var compo = jsonObj.results[0].address_components; for (var i = 0; i < compo.length; i++) {for (var j = 0; j < compo[i].types.length; j++) { if (compo[i].types[j] == 'administrative_area_level_1') {return compo[i].long_name;} } } }"
    scriptControl.AddCode "function getCountry(jsonObj) { if(jsonObj.results[0] === undefined) return -1; var compo = jsonObj.results[0].address_components; for (var i = 0; i < compo.length; i++) {for (var j = 0; j < compo[i].types.length; j++) { if (compo[i].types[j] == 'country') {return compo[i].long_name;} } } }"
    scriptControl.AddCode "function getLat(jsonObj) { if(jsonObj.results[0] === undefined) return -1; return jsonObj.results[0].geometry.location.lat;}"
    scriptControl.AddCode "function getLng(jsonObj) { if(jsonObj.results[0] === undefined) return -1; return jsonObj.results[0].geometry.location.lng;}"

    For i = 3 To 3531

    request = "https://maps.googleapis.com/maps/api/geocode/json?address=%22" & Cells(i, 2) & "%22&key="

    If Cells(i, 3).Value2 = "NA" Then
    With CreateObject("MSXML2.XMLHTTP")
        .Open "GET", SupprimerAccents(request), False
        .send
        Set Address = scriptControl.Eval("(" + .responseText + ")")
        r = .responseText
    End With
    Debug.Print r
    Cells(i, 5) = scriptControl.Run("getLocality", Address, "results")
    Cells(i, 4) = scriptControl.Run("getRegion", Address, "results")
    Cells(i, 3) = scriptControl.Run("getCountry", Address, "results")
    Cells(i, 6) = scriptControl.Run("getLat", Address, "results")
    Cells(i, 7) = scriptControl.Run("getLng", Address, "results")
    End If

    Next i

End Sub
