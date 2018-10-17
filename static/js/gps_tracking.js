$(function () {
    var map, marker, poly, watchId;

    var isTracking = false; //現在GPSで位置情報を取得しているかどうかを判断するフラグ
    var track_ptr = 1; //next pointer
    var track_flag = false;
    const L = 30; //設定経路からの距離の許容範囲

    var nodes = []
    var points = [];

    for (var i = 0; i < data.length; i++) {
        nodes.push(data[i]);
        points.push(new google.maps.LatLng(nodes[i].lat, nodes[i].lng));
    }
    var geoOptions = {
        enableHighAccuracy: true,
        timeout: 60000,
        maximumAge: 0
    };


    function initMap() {
        displayData(nodes[0].lat, nodes[0].lng, null);
        var latlng = new google.maps.LatLng(nodes[0].lat, nodes[0].lng);
        var mapOptions = {
            zoom: 10,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);
        marker = new google.maps.Marker({
            position: latlng,
            map: map,
            optimized: false,
        });
        //ここにマップ描画を書く
        var d = new google.maps.DirectionsService(); // ルート検索オブジェクト
        var origin = null,
            waypoints = [],
            dest = null; // 出発地、経由地、目的地
        var resultMap = {}; // 分割してルート検索した結果データ
        var requestIndex = 0; // 検索番号
        var done = 0; // ルート検索が完了した数
        for (var i = 0, len = points.length; i < len; i++) {
            // 最初の場合、originに値をセット
            if (origin == null) {
                origin = points[i];
            }
            // 経由地が8つたまったか最後の地点の場合、ルート検索
            else if (waypoints.length == 8 || i == len - 1 || nodes[i].flag == true) {
                dest = points[i];

                (function (index) {
                    // ルート検索の条件
                    var request = {
                        origin: origin, // 出発地
                        destination: dest, // 目的地
                        waypoints: waypoints, // 経由地
                        travelMode: google.maps.DirectionsTravelMode.WALKING, // 交通手段(歩行。DRIVINGの場合は車)
                    };
                    // ルート検索
                    d.route(request, function (result, status) {
                        // OKの場合ルートデータ保持
                        if (status == google.maps.DirectionsStatus.OK) {
                            resultMap[index] = result; // 並行でリクエストするので配列だとリクエスト順とずれる場合があります
                            done++;
                        } else {
                            console.log(status); // デバッグ
                        }
                    });
                })(requestIndex);

                requestIndex++;
                origin = points[i]; // 今回の目的地を次回の出発地にします。
                waypoints = [];
            }
            // 上記以外、waypointsに地点を追加
            else {
                waypoints.push({
                    location: points[i],
                    stopover: false
                });
            }
        }

        // マーカーを表示する場合の準備
        var infoWindow = new google.maps.InfoWindow();
        var mark = function (position, content) {
            var marker = new google.maps.Marker({
                map: map, // 描画先の地図
                position: position // 座標
            });
            // クリック時吹き出しを表示
            marker.addListener("click", function () {
                infoWindow.setContent(content);
                infoWindow.open(map, marker);
            });
        };

        var sid = setInterval(function () {
            // 分割したすべての検索が完了するまで待ちます。
            if (requestIndex > done) return;
            clearInterval(sid);

            // すべての結果のルート座標を順番に取得して平坦な配列にします。
            var path = [];
            var result;
            for (var i = 0, len = requestIndex; i < len; i++) {
                result = resultMap[i]; // 検索結果
                var legs = result.routes[0].legs; // Array<DirectionsLeg>
                for (var li = 0, llen = legs.length; li < llen; li++) {
                    var leg = legs[li]; // DirectionLeg
                    var steps = leg.steps; // Array<DirectionsStep>
                    // DirectionsStepが持っているpathを取得して平坦化(2次元配列→1次元配列)。
                    var _path = steps.map(function (step) {
                            return step.path
                        })
                        .reduce(function (all, paths) {
                            return all.concat(paths)
                        });
                    path = path.concat(_path);

                    // マーカーが必要ならマーカーを表示します。
                    mark(leg.start_location, leg.start_address); //すごろくイベントを第２引数とする
                }
            }
            // マーカーが必要ならマーカーを表示します。(最終)
            var endLeg = result.routes[0].legs[result.routes[0].legs.length - 1];
            mark(endLeg.end_location, endLeg.end_address); //すごろくイベントを第２引数とする

            // パスを描画します。
            var line = new google.maps.Polyline({
                map: map, // 描画先の地図
                strokeColor: "#2196f3", // 線の色
                strokeOpacity: 0.8, // 線の不透明度
                strokeWeight: 6, // 先の太さ
                path: path // 描画するパスデータ
            });
        }, 1000);
    }

    function updateMap(position) {
        console.log(isTracking); //デバッグ用
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var accu = position.coords.accuracy;

        displayData(lat, lng, accu);

        var latlng = new google.maps.LatLng(lat, lng);
        map.setCenter(latlng);
        marker.setPosition(latlng);
        if (lat == nodes[track_ptr].lat && lng == nodes[track_ptr].lng) {
            track_ptr++;
            console.log(track_ptr); //デバッグ用
        }
        if (track_ptr > nodes.length) {
            navigator.geolocation.clearWatch(watchId);
            console.log("終了"); //デバッグ用
        } //トラッキング終了
        track_flag = positionCheck(lat, lng); //デバッグ用
        console.log(track_flag); //デバッグ用


    }

    // データを表示する displayData 関数(デバッグ用)
    function displayData(lat, lng, accu) {
        var txt = document.getElementById("txt"); // データを表示するdiv要素の取得
        txt.innerHTML = "緯度, 経度: " + lat + ", " + lng + "<br>" // データ表示
            +
            "精度: " + accu;
    }

    function positionCheck(lat, lng) { //通知をするかをチェックする
        // 距離
        var d = google.maps.geometry.spherical.computeDistanceBetween(points[track_ptr], points[track_ptr - 1]);
        console.log(d); //デバッグ用
        var r = google.maps.geometry.spherical.computeDistanceBetween(points[track_ptr], new google.maps.LatLng(lat, lng));
        console.log(r); //デバッグ用
        var rad = Math.acos(d / r);
        console.log(rad); //デバッグ用
        var l = r * Math.sin(rad);
        console.log(l); //デバッグ用
        if (l > L) {
            return true;
        }
        return false;

    }

    //継続的な位置の取得の開始
    function startPositionTracking() {
        watchId = navigator.geolocation.watchPosition(updateMap, null, geoOptions);
        isTracking = true;
    }

    //継続的な位置の取得の停止
    function stopPositionTracking() {
        navigator.geolocation.clearWatch(watchId);
        isTracking = false;
    }

    initMap();
    startPositionTracking();

});
