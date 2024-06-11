import React from "react";

const Footer = () => {
  // 첫 페이지일 때만 Footer를 렌더
  const isHomePage = window.location.pathname === '/';

  
  if (!isHomePage) return null;

  return (
    <footer className="page-footer font-small blue pt-4">
      <div className="container text-center">
        <h5 className="text-uppercase">안녕하세요, KHIS 병원입니다</h5>
        <img src="/image/병원 배너 사진.jpeg" alt="병원 배너 사진" className="footer-banner" />
        
        <div className="row mt-4">
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title text-uppercase">예약하기</h5>
                <ul className="list-unstyled">
                  <li><a href="/appointment">바로가기</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title text-uppercase">병원 일정</h5>
                <ul className="list-unstyled">
                  <li><a href="/schedule">바로가기</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title text-uppercase">대기열</h5>
                <ul className="list-unstyled">
                  <li><a href="/waiting-list">바로가기</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title text-uppercase">AI 챗봇 </h5>
                <ul className="list-unstyled">
                  <li><a href="/chatbot">바로가기</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
