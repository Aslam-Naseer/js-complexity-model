

SIMPLE_CASE = """
// ============================================================
// SIMPLE (Low Complexity)
// Profile: Linear logic, no loops, minimal variables.
// ============================================================

function calculateFinalPrice(basePrice, taxRate, discount) {
    const taxAmount = basePrice * taxRate;
    const priceWithTax = basePrice + taxAmount;
    let finalTotal = priceWithTax - discount;

    if (finalTotal < 0) {
        finalTotal = 0;
    }

    return finalTotal;
}
"""

MODERATE_CASE = """
// ============================================================
// MODERATE (Medium Complexity)
// Profile: Single nested loop, multiple conditionals, array building.
// ============================================================

function generateUserReport(users, activeThreshold, region) {
    let reportData = [];
    let skippedCount = 0;
    let totalAge = 0;
    
    // Loop 1 (Depth 1)
    for (let i = 0; i < users.length; i++) {
        let user = users[i];
        
        // Conditional (Depth 2)
        if (user.region === region) {
            
            // Nested Conditional (Depth 3)
            if (user.activityScore >= activeThreshold) {
                // Logic/Statement density
                let formattedName = user.lastName + ", " + user.firstName;
                let status = "Active";
                totalAge += user.age;
                
                reportData.push({
                    id: user.id,
                    name: formattedName,
                    status: status
                });
            } else {
                skippedCount++;
            }
        }
    }

    // Additional statement block
    let averageAge = 0;
    if (reportData.length > 0) {
        averageAge = totalAge / reportData.length;
    }

    return { data: reportData, skipped: skippedCount, avg: averageAge };
}
"""

COMPLEX_CASE = """
// ============================================================
// COMPLEX (High Complexity)
// Profile: Deep nesting (7 levels), heavy variable tracking, no helper functions.
// ============================================================

function analyzeGridStability(gridMatrix, config, timeDelta) {
    let unstableZones = 0;
    let maxPressure = 0;
    let criticalErrors = [];
    const rows = gridMatrix.length;
    const cols = gridMatrix[0].length;
    const limit = config.pressureLimit;

    // Loop 1: Rows (Depth 1)
    for (let r = 0; r < rows; r++) {
        
        // Loop 2: Columns (Depth 2)
        for (let c = 0; c < cols; c++) {
            let cell = gridMatrix[r][c];
            
            // Conditional 1 (Depth 3)
            if (cell !== null && typeof cell === 'object') {
                let currentPressure = cell.basePressure + (cell.flux * timeDelta);
                
                // Conditional 2 (Depth 4)
                if (cell.isActive) {
                    
                    // Complex Logic block
                    let tempMod = 1.0;
                    if (config.temperature > 100) tempMod = 1.5;
                    currentPressure = currentPressure * tempMod;

                    // Conditional 3 (Depth 5) - Threshold Check
                    if (currentPressure > limit) {
                        
                        // Conditional 4 (Depth 6) - Neighbor Check (Manually expanded logic)
                        if (r > 0 && gridMatrix[r-1][c] && gridMatrix[r-1][c].isActive) {
                            let neighborPress = gridMatrix[r-1][c].basePressure;
                            
                            // Conditional 5 (Depth 7) - The Deepest Point
                            if ((currentPressure - neighborPress) > config.criticalDiff) {
                                unstableZones++;
                                criticalErrors.push(`Critical Delta at ${r},${c}`);
                                
                                // Reset logic
                                cell.isActive = false;
                                currentPressure = 0;
                            }
                        }
                        
                        // Fallback logic (Depth 6 alternate)
                        if (currentPressure > maxPressure) {
                            maxPressure = currentPressure;
                        }
                    }
                }
            } else {
                // Handling invalid data (Statement padding)
                criticalErrors.push(`Invalid Cell at ${r},${c}`);
            }
        }
    }

    // Final calculations
    let safetyRating = "Safe";
    if (unstableZones > 5) safetyRating = "Caution";
    if (unstableZones > 20) safetyRating = "Danger";

    return { 
        zones: unstableZones, 
        peak: maxPressure, 
        rating: safetyRating, 
        errors: criticalErrors.length 
    };
}
"""

DEFAULT_CODE_SNIPPET = f"{SIMPLE_CASE} \n {MODERATE_CASE} \n {COMPLEX_CASE}"
