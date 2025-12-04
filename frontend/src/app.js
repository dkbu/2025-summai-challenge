import BpmnJS from 'bpmn-js/lib/Modeler';
import { useEffect, useRef, useState } from 'react';

// Function that returns a working instance of BpmnJS
export function createBpmnModeler(container) {
    const modeler = new BpmnJS({
        container: container,
        keyboard: {
            bindTo: window
        }
    });

    return modeler;
}

export default function App() {
    const [server_url, setServerUrl] = useState("http://127.0.0.1:8000");
    const [userCount, setUserCount] = useState(0);
    const [diagramXML, setDiagramXML] = useState(null);

    const containerRef = useRef(null);
    const modelerRef = useRef(null);

    useEffect(() => {
        let intervalCounterId = null;
        let intervalDiagramId = null;

        // Handle browser/tab closing
        const handleBeforeUnload = (event) => {
            // Perform cleanup when browser is closing
            if (modelerRef.current) {
                // Use sendBeacon with a special endpoint for cleanup
                // sendBeacon only supports POST, so we'll send action info in the body
                const cleanupData = new Blob(
                    [JSON.stringify({ action: 'remove_user' })],
                    { type: 'application/json' }
                );

                // sendBeacon is the most reliable way for cleanup during unload
                if (navigator.sendBeacon) {
                    navigator.sendBeacon(`${server_url}/cleanup`, cleanupData);
                }
            }
        };

        // Add the beforeunload event listener
        window.addEventListener('beforeunload', handleBeforeUnload);

        setTimeout(() => {
            if (containerRef.current && !modelerRef.current) {
                addUser()
                    .then(() => {
                        try {
                            // Create BpmnJS instance using our function
                            initializeBpmnModeler();

                            // Start the user count fetching interval after successful initialization
                            intervalCounterId = setInterval(() => {
                                fetchUserCount();
                            }, 1000);

                            // Fetch the initial diagram
                            intervalDiagramId = setInterval(() => {
                                fetchDiagram();
                            }, 100);

                        } catch (error) {
                            console.error('Error initializing BPMN modeler:', error);
                        }
                    }).catch(err => {
                        console.error('Error adding user:', err);
                    });
            }
        }, 50);

        // Cleanup on unmount
        return () => {
            // Remove the beforeunload event listener
            window.removeEventListener('beforeunload', handleBeforeUnload);

            // Clear the interval
            if (intervalCounterId) {
                clearInterval(intervalCounterId);
            }

            if (intervalDiagramId) {
                clearInterval(intervalDiagramId);
            }

            // Clean up BPMN modeler and remove user
            if (modelerRef.current) {
                removeUser();
                modelerRef.current.destroy();
                modelerRef.current = null;
            }
        };
    }, [server_url]);

    function onModelChanged(event) {
        console.log('Model changed');
        modelerRef.current.saveXML({ format: true }).then(({ xml }) => {
            fetch(`${server_url}/diagram`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "new_diagram": xml }) 
            });
        }).catch(err => {
            console.error('Error saving BPMN XML:', err);
        });
    }

    function fetchDiagram() {
        fetch(`${server_url}/diagram`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                const xml = data.diagram;
                if (xml) {
                    setDiagramXML(xml);
                }
            });
    }

    function fetchUserCount() {
        fetch(`${server_url}/users`, { method: 'GET' })
            .then(response => {
                console.log('Fetch user count response status:', response.status);
                return response.json();
            })
            .then(data => {
                setUserCount(data.user_count);
            })
            .catch(error => {
                console.error('Error fetching user count:', error);
            });
    }

    function removeUser() {
        fetch(`${server_url}/user`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                console.log('User removed:', data);
            })
            .catch(error => {
                console.error('Error removing user:', error);
            });
    }

    async function addUser() {
        fetch(`${server_url}/user`, {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                console.log('User added:', data);
            })
            .catch(error => {
                return new Error('Error adding user:', error);
            });
    }

    useEffect(() => {
        if (diagramXML && modelerRef.current) {
            importDiagram();
        }
    }, [diagramXML]);


    function importDiagram() {
        let diagram = null;
        if (!diagramXML) {
            diagram = modelerRef.current.createDiagram();
        }
        else {
            diagram = modelerRef.current.importXML(diagramXML);
        }

        return diagram;
    }

    function initializeBpmnModeler() {
        modelerRef.current = createBpmnModeler(containerRef.current);

        let diagram = importDiagram();

        // hook into events
        var eventBus = modelerRef.current.get('eventBus');
        var events = [
            'element.hover',
            'element.out',
            'element.click',
            'element.dblclick',
            'element.mousedown',
            'element.mouseup'
        ];

        events.forEach(function (event) {

            eventBus.on(event, onModelChanged);
        });

        return diagram;
    }

    return (
        <div>
            <h1>Summai Challenge - BPMN Editor</h1>
            <div>{userCount} users connected.</div>
            <div
                ref={containerRef}
                id="canvas"
                style={{
                    width: '100%',
                    height: '600px',
                    border: '1px solid #ccc'
                }}
            />
        </div>
    );
}


