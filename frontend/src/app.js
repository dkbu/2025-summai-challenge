import BpmnJS from 'bpmn-js/lib/Modeler';
import React, { useEffect, useRef } from 'react';

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
    const containerRef = useRef(null);
    const modelerRef = useRef(null);

    useEffect(() => {
        if (containerRef.current && !modelerRef.current) {
            // Small delay to ensure container is fully rendered
            setTimeout(() => {
                try {
                    // Create BpmnJS instance using our function
                    modelerRef.current = createBpmnModeler(containerRef.current);
                    
                    return modelerRef.current.createDiagram();
                } catch (error) {
                    console.error('Error initializing BPMN modeler:', error);
                }
            }, 50); // Small delay to ensure DOM is ready
        }

        // Cleanup on unmount
        return () => {
            if (modelerRef.current) {
                modelerRef.current.destroy();
            }
        };
    }, []);

    return (
        <div>
            <h1>Summai Challenge - BPMN Editor</h1>
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