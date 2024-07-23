import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './Dashboard.css';

const Dashboard = ({ onLogout }) => (
  <Container fluid>
    <Row>
      <Col xs={12} md={3} className="bg-dark text-white p-3">
        <h3>Dashboard</h3>
        <ul className="list-unstyled">
          <li className="mb-2">
            <Link to="/upload" className="text-white text-decoration-none">
              <Button variant="light" className="w-100">Upload Document</Button>
            </Link>
          </li>
          <li className="mb-2">
            <Link to="/documents/:id/" className="text-white text-decoration-none">
              <Button variant="light" className="w-100">View Document</Button>
            </Link>
          </li>
          <li className="mb-2">
            <Button variant="danger" className="w-100" onClick={onLogout}>Logout</Button>
          </li>
        </ul>
      </Col>
      <Col xs={12} md={9} className="p-3">
        <Outlet />
      </Col>
    </Row>
  </Container>
);

export default Dashboard;
