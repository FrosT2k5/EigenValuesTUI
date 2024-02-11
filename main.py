import pytermgui as ptg
from re import match
from sympy import Matrix
from time import sleep

def inputMatrix(numberOfRows: int):
    box = ptg.Container()
    box.set_char("border",["|"," ","|"," "])
    #box.set_char("corner",["--- "+"Enter Matrix", "---", "---", "---"])

    for i in range(numberOfRows):
        rowTuple = []
        for j in range(numberOfRows):
            inputField = ptg.InputField("   ",prompt="")
            inputField.bind(ptg.keys.CARRIAGE_RETURN, lambda *_: None)
            inputField.bind(ptg.keys.ENTER, lambda *_: None) 

            rowTuple += inputField
        box += tuple(rowTuple)
        box += ""

    return box.center()

def exitProgram(manager: ptg.WindowManager, window: ptg.Window):
    window.close()
    sleep(0.85)
    manager.stop()
    exit(0)

def InfoWindow(manager: ptg.WindowManager, text: str, answer=None) -> None:
    outString = "[red]" + text
    if answer:
        outString += "[skyblue bold]" + str(answer)

    modal = ptg.Window(
        "",
        outString,
        "",
        ptg.Button("Ok", lambda *_: modal.close()),
        "",
        width=len(outString)+10
    ).center()

    modal.bind("q", lambda *_: exitProgram(manager, modal))
    modal.select(1)
    manager.add(modal)

def showEigenVectors(manager: ptg.WindowManager, window: ptg.Window, eigVects: list) -> None:
    newWindow = ptg.Window(
        "",
        "Eigen Vectors: ",
        "",
    ).center()

    window.close()

    for vect in eigVects:
        outStr = ""
        for val in vect:
            outStr += str(val) + "  "

        label = ptg.Label("=> "+ outStr + "<=")
        newWindow.__add__(label)
    
    def restart():
        newWindow.close()
        main(manager)

    newWindow.__add__("")
    newWindow.__add__(ptg.Button("Ok", lambda *_: restart()))
    newWindow.__add__("")
    newWindow.bind("q", lambda *_: exitProgram(manager, newWindow))
    manager.add(newWindow)
    
def matrixSubmit(manager: ptg.WindowManager, window: ptg.Window, noOfRows: int):
    userInput = []
    box = window[1]

    for i in range(len(box)):
        try:
            length = len(box[i])
        except:
            length = 0
        for j in range(length):
            try:
                val = int(box[i][j].value)
                userInput.append(val)
            except:
                None

    if len(userInput) < noOfRows**2:
        InfoWindow(manager, "Please input all elements of matrix", "")
        return

    mat = Matrix(noOfRows,noOfRows,userInput)

    eigValues = mat.eigenvals()
    eigVects = mat.eigenvects()
    eigenValuesStr = ""
    eigenValuesCount = 0
    for i in eigValues:
        eigenValuesStr += str(i) + " , "
        eigenValuesCount += 1
    eigenValuesStr = eigenValuesStr[:-2]

    derogatoryText = ""
    if noOfRows > eigenValuesCount:
        derogatoryText = "Eigen values are repeated, \nMatrix is Derogatory"
    else:
        derogatoryText = "Eigen values are not repeated, \nMatrix is NOT Derogatory"

    window.close()
    eigenValueWindow = ptg.Window(
        "",
        ptg.Label("Eigen values are: "),
        "",
        ptg.Label(eigenValuesStr),
        "",
        ptg.Label(derogatoryText),
        "",
        ["Submit", lambda *_: showEigenVectors(manager, eigenValueWindow, eigVectsList)],
        "",
        ""
    ).center()
    eigenValueWindow.bind("q", lambda *_: exitProgram(manager, eigenValueWindow))

    eigVectsList = []
    for i in range(len(eigVects)):
        eigVectsList.append(eigVects[i][2][0])
    
    #eigenValueWindow.bind(ptg.keys.ENTER, showEigenVectors(manager, eigenValueWindow, eigVectsList))
    manager.add(eigenValueWindow)


def noOfRowsSubmit(manager: ptg.WindowManager, window: ptg.Window) -> None:
    inputValue = window[1].value
    
    if not match("^[0-5]$",inputValue):
        InfoWindow(manager, "Please enter a correct value, Number between 1 to 5: "+ inputValue)
        return

    noOfRows = int(inputValue)
    box = inputMatrix(noOfRows)
    manager.remove(window)

    window = (
        ptg.Window(
            "",
            box,
            "",
            "",
            ["Submit", lambda *_: matrixSubmit(manager, window, noOfRows)],
            ""
        )
        .set_title("[210 bold]Enter matrix.")
        .center()
    )
    window.bind(ptg.keys.CARRIAGE_RETURN, lambda *_: matrixSubmit(manager, window, noOfRows))
    window.bind(ptg.keys.ENTER, lambda *_: matrixSubmit(manager, window, noOfRows))
    window.bind("q", lambda *_: exitProgram(manager, window))

    manager.add(window)

def main(manager: ptg.WindowManager):

    inputField = ptg.InputField("", prompt="No of rows in square matrix: ")

    window = (
        ptg.Window(
            "",
            inputField,
            "",
            "",
            "",
            ["Submit", lambda *_: noOfRowsSubmit(manager, window)],
            "",
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]Eigen Values and Eigen Vectors Calculator.")
        .center()
    )

    inputField.bind(ptg.keys.CARRIAGE_RETURN, lambda *_: noOfRowsSubmit(manager, window))
    inputField.bind(ptg.keys.ENTER, lambda *_: noOfRowsSubmit(manager, window))
    window.bind("q", lambda *_: exitProgram(manager, window))

    manager.add(window)

if __name__ == "__main__":
    with ptg.WindowManager() as manager:
        main(manager)
