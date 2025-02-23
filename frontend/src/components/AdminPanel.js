import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Table, Form, Modal } from 'react-bootstrap';

export default function AdminPanel() {
    const [faqs, setFaqs] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [editFaq, setEditFaq] = useState({ question: '', answer: '' });

    useEffect(() => {
        axios.get('http://localhost:5000/faqs')
            .then(res => setFaqs(res.data))
            .catch(console.error);
    }, []);

    const handleSubmit = () => {
        if (editFaq.id) {
            axios.put(`http://localhost:5000/faqs/${editFaq.id}`, editFaq)
                .then(() => {
                    setFaqs(faqs.map(f => f.id === editFaq.id ? editFaq : f));
                    setShowModal(false);
                });
        } else {
            axios.post('http://localhost:5000/faqs', editFaq)
                .then(res => {
                    setFaqs([...faqs, { ...editFaq, id: res.data.id }]);
                    setShowModal(false);
                });
        }
    };

    const deleteFaq = (id) => {
        axios.delete(`http://localhost:5000/faqs/${id}`)
            .then(() => setFaqs(faqs.filter(f => f.id !== id)));
    };

    return (
        <div>
            <Button onClick={() => { setEditFaq({}); setShowModal(true); }}>
                Add New FAQ
            </Button>

            <Table striped>
                <thead>
                    <tr>
                        <th>Question</th>
                        <th>Answer</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {faqs.map(faq => (
                        <tr key={faq.id}>
                            <td>{faq.question}</td>
                            <td>{faq.answer}</td>
                            <td>
                                <Button variant="warning" onClick={() => { 
                                    setEditFaq(faq); 
                                    setShowModal(true);
                                }}>
                                    Edit
                                </Button>
                                <Button variant="danger" onClick={() => deleteFaq(faq.id)}>
                                    Delete
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>{editFaq.id ? 'Edit' : 'New'} FAQ</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group>
                            <Form.Label>Question</Form.Label>
                            <Form.Control 
                                value={editFaq.question}
                                onChange={e => setEditFaq({...editFaq, question: e.target.value})}
                            />
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Answer</Form.Label>
                            <Form.Control as="textarea" rows={3}
                                value={editFaq.answer}
                                onChange={e => setEditFaq({...editFaq, answer: e.target.value})}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleSubmit}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
