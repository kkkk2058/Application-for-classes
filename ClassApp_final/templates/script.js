// $(document).ready(function(){
//     const path = window.location.pathname;

//     // cartvis.html 관련 스크립트
//     if (path.includes('cartvis')) {
//         initializeCartVis();
//     }

//     // firstPage.html 관련 스크립트
//     if (path.includes('firstPage')) {
//         initializeFirstPage();
//     }

//     // sstatus.html 관련 스크립트
//     if (path.includes('sstatus')) {
//         initializeSstatus();
//     }

//     // sbuket.html 관련 스크립트
//     if (path.includes('buket')) {
//         initializeSbucket();
//     }
// });

// // cartvis.html 관련 함수
// function initializeCartVis() {
//     loadVisualization(1); // 기본 우선순위 1로 로드
    
//     $(".btn-group-vertical button").click(function(){
//         var priority = $(this).text().match(/\d+/)[0]; // 버튼의 텍스트에서 숫자 추출
//         loadVisualization(priority);
//     });
// }

// function loadVisualization(priority) {
//     $.ajax({
//         url: "/cartvis/get_vis_html",
//         type: "get",
//         data: { priority: priority },
//         success: function(response){
//             $("#visualization").html(response); // 응답으로 받은 HTML을 영역에 삽입
//         }
//     });
// }

// // firstPage.html 관련 함수
// function initializeFirstPage() {
//     const scoresSet = [
//         [100, 100, 100, 100, 100], // 첫 번째 점수 세트 (모든 점수 100)
//         scoresFromServer  // 서버에서 전달된 점수 세트
//     ];

//     const labels = ["강의 평점", "과제량", "시험 난이도", "강의 시간", "팀플"];
//     const colors = ["white", "skyblue"];
//     const maxScore = 100;
//     const center = { x: 200, y: 200 };
//     const radius = 150;
//     const labelOffset = 30;

//     drawPolygon(scoresSet, labels, colors, maxScore, center, radius, labelOffset);

//     function fetchCartItems() {
//         $.ajax({
//             url: '/buket/get_cart', // Endpoint to fetch cart items
//             type: 'GET',
//             success: function(response) {
//                 displayCartItems(response); // Pass the fetched data to display function
//             },
//             error: function(error) {
//                 console.error('Error fetching cart items:', error);
//             }
//         });
//     }

//     function displayCartItems(cartItems) {
//         var cartHtml = '<h2>내 장바구니</h2><ul class="list-group">';

//         cartItems.forEach(function(item) {
//             cartHtml += '<li class="list-group-item">' + item.subject + '</li>';
//         });

//         cartHtml += '</ul>';
//         $('#cart').html(cartHtml);
//     }

//     $(document).ready(function() {
//         fetchCartItems();
//     });
// }

// function drawPolygon(scoresSet, labels, colors, maxScore, center, radius, labelOffset) {
//     const svg = document.getElementById('statusPolygon');
//     svg.innerHTML = '';

//     scoresSet.forEach((scores, idx) => {
//         const points = calculatePoints(scores, maxScore, center, radius);
//         const pointsAttr = points.map(p => `${p.x},${p.y}`).join(' ');

//         svg.innerHTML += `<polygon points="${pointsAttr}" style="fill:${colors[idx]};stroke:purple;stroke-width:1" />`;

//         if (idx === 0) {
//             const labelPoints = calculatePoints(scores, maxScore, center, radius, labelOffset);
//             labelPoints.forEach((point, labelIdx) => {
//                 svg.innerHTML += `<text x="${point.x}" y="${point.y}" fill="black" text-anchor="middle" alignment-baseline="central">${labels[labelIdx]}</text>`;
//             });
//         }
//     });
// }

// function calculatePoints(scores, maxScore, center, radius, offset = 0) {
//     const points = [];
//     const angleIncrement = (Math.PI * 2) / scores.length;

//     scores.forEach((score, index) => {
//         const angle = angleIncrement * index - Math.PI / 2;
//         const scoreRadius = (score / maxScore) * radius + offset;
//         const x = center.x + scoreRadius * Math.cos(angle);
//         const y = center.y + scoreRadius * Math.sin(angle);
//         points.push({x, y});
//     });

//     return points;
// }

// // sstatus.html 관련 함수
// function initializeSstatus() {
//     $('form').submit(function(event) {
//         event.preventDefault(); // 기본 동작 방지
//         var subjectName = $('#subject').val(); // 입력된 과목명 가져오기

//         $.get('/subject/' + subjectName, function(data) {
//             if (data.error) {
//                 $('#searchResult').html('<p>' + data.error + '</p>');
//             } else {
//                 let scoresSet = [
//                     [100, 100, 100, 100, 100], // 첫 번째 점수 세트 (모든 점수 100)
//                     [
//                         data.lectureRating,
//                         data.assignmentCount,
//                         data.examDifficulty,
//                         parseFloat(data.lectureTime),
//                         parseFloat(data.studentCount)
//                     ]
//                 ];

//                 const labels = ["전체평점", "과제량", "시험 난이도", "강의 시간", "팀플"];
//                 const colors = ["white", "skyblue"];
//                 const maxScore = 100;
//                 const center = { x: 200, y: 200 };
//                 const radius = 150;
//                 const labelOffset = 30;

//                 drawPolygon(scoresSet, labels, colors, maxScore, center, radius, labelOffset);

//                 var subjectHtml = '<ul class="nav flex-column">';
//                 subjectHtml += '<li class="nav-item"><a class="nav-link" href="#">강의 평점: ' + data.lectureRating + '/100</a></li>';
//                 subjectHtml += '<li class="nav-item"><a class="nav-link" href="#">과제량: ' + data.assignmentCount + '/100</a></li>';
//                 subjectHtml += '<li class="nav-item"><a class="nav-link" href="#">시험 난이도: ' + data.examDifficulty + '/100</a></li>';
//                 subjectHtml += '<li class="nav-item"><a class="nav-link" href="#">강의 시간: ' + data.lectureTime + '/100</a></li>';
//                 subjectHtml += '<li class="nav-item"><a class="nav-link" href="#">팀플: ' + data.studentCount + '/100</a></li>';
//                 subjectHtml += '</ul>';

//                 $('#searchResult').html(subjectHtml);
//             }
//         });
//     });
// }

// // sbuket.html 관련 함수
// function initializeSbucket() {
//     let cart = []; // 장바구니 배열을 정의하고 초기화합니다.
//     let courses = []; // 서버에서 가져온 데이터를 담을 배열

//     async function fetchCourses() {
//         try {
//             const response = await fetch('/buket/get_subs'); // get_subs 엔드포인트에서 데이터를 가져옴
//             const data = await response.json(); // JSON 형식으로 파싱
//             courses = data; // 가져온 데이터를 courses 배열에 저장
//             searchCourses(); // 데이터 가져온 후 화면 업데이트
//             fetchCart(); // Fetch cart contents
//         } catch (error) {
//             console.error('데이터를 가져오는 중 오류 발생:', error);
//         }
//     }

//     async function fetchCart() {
//         try {
//             const response = await fetch('/buket/get_cart'); // get_cart 엔드포인트에서 데이터를 가져옴
//             const data = await response.json(); // JSON 형식으로 파싱
//             cart = data; // 가져온 데이터를 cart 배열에 저장
//             updateCart(); // 데이터 가져온 후 장바구니 업데이트
//         } catch (error) {
//             console.error('장바구니 데이터를 가져오는 중 오류 발생:', error);
//         }
//     }

//     function searchCourses() {
//         const input = document.getElementById('searchInput').value.toLowerCase();
//         const filteredCourses = courses.filter(course => course.name.toLowerCase().includes(input));
//         const coursesList = document.getElementById('coursesList');
//         coursesList.innerHTML = '';

//         filteredCourses.forEach(course => {
//             const row = document.createElement('tr');
//             row.innerHTML = `<td>${course.name}</td>
//                             <td>${course.competition}</td>
//                             <td>${course.rankInfo.replace(/,\s+/g, ', ')}</td>
//                             <td>${course.gradeInfo}</td>
//                             <td>
//                                 <select class="form-control form-control-sm" id="priority-${course.id}">
//                                     <option value="1">1</option>
//                                     <option value="2">2</option>
//                                     <option value="3">3</option>
//                                     <option value="4">4</option>
//                                     <option value="5">5</option>
//                                 </select>
//                             </td>
//                             <td><button onclick="addToCart(${course.id})" class="btn btn-success btn-sm">장바구니에 추가</button></td>`;
//             coursesList.appendChild(row);
//         });
//     }

//     function addToCart(courseId) {
//         const priority = document.getElementById(`priority-${courseId}`).value;
//         $.ajax({
//             url: '/buket/add',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({ sbj_id: courseId, priority: priority }),
//             success: function(response) {
//                 if (response.message) {
//                     alert(response.message); // Display success message
//                     fetchCart(); // Re-fetch cart to update the list
//                 } else {
//                     alert('Failed to add course to cart');
//                 }
//             },
//             error: function(error) {
//                 if (error.status === 409) {  // Conflict error code
//                     alert('Course already in cart');
//                 } else {
//                     alert('Error adding course to cart');
//                 }
//                 console.error('Error:', error);
//             }
//         });
//     }

//     function removeFromCart(courseId) {
//         $.ajax({
//             url: '/buket/remove',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({ sbj_id: courseId }),
//             success: function(response) {
//                 fetchCart(); // Re-fetch cart to update the list
//             },
//             error: function(error) {
//                 alert('Error removing course from cart');
//                 console.error(error);
//             }
//         });
//     }

//     function updateCart() {
//         const cartList = document.getElementById('cartList');
//         cartList.innerHTML = '';
//         cart.forEach(course => {
//             const li = document.createElement('li');
//             li.className = 'list-group-item';
//             li.innerHTML = `${course.subject} 
//                             <button onclick="removeFromCart(${course.sbj_id})" class="btn btn-sm btn-danger float-right">장바구니에서 제거</button>`;
//             cartList.appendChild(li);
//         });
//     }

//     window.onload = fetchCourses;
// }
