import pytermgui as ptg
from re import match
from sympy import Matrix

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

    with open("file.txt","w") as f:
            f.write(str(box[1]))
    return box.center()

def InfoWindow(manager: ptg.WindowManager, text: str, answer=None) -> None:
    outString = "[red]" + text
    if answer:
        outString += "[skyblue bold]" + str(answer)

    modal = ptg.Window(
        outString,
        "",
        ptg.Button("Ok", lambda *_: modal.close()),
        width=len(outString)+10
    ).center()

    modal.select(1)
    manager.add(modal)

def showEigenVectors(manager: ptg.WindowManager, window: ptg.Window) -> None:
    None

def matrixSubmit(manager: ptg.WindowManager, window: ptg.Window, noOfRows: int):
    userInput = []
    box = window[0]

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
    
    # with open('file.txt','w') as f:
    #     f.write(str(userInput))
    # outputField = ptg.Label(str(userInput))
    # window.__add__(outputField)

    mat = Matrix(noOfRows,noOfRows,userInput)
    eigValues = mat.eigenvals()
    eigVects = mat.eigenvects()
    eigenValuesStr = ""
    for i in eigValues:
        eigenValuesStr += str(i) + " "

    eigenValueWindow = ptg.Window(
        "",
        ptg.Label("Eigen values are: "),
        "",
        "",
        ptg.Label(eigenValuesStr),
        "",
        ["Submit", lambda *_: showEigenVectors(manager, window)],
    ).center()
    manager.add(eigenValueWindow)


def noOfRowsSubmit(manager: ptg.WindowManager, window: ptg.Window) -> None:
    inputValue = window[1].value
    
    if not match("[0-5]",inputValue):
        InfoWindow(manager, "Please enter a correct value, Number between 1 to 5: "+ inputValue)
        return

    noOfRows = int(inputValue)    
    box = inputMatrix(noOfRows)
    manager.remove(window)

    window = (
        ptg.Window(
            box,
            "",
            "",
            ["Submit", lambda *_: matrixSubmit(manager, window, noOfRows)]
        )
        .set_title("[210 bold]Enter matrix.")
        .center()
    )
    
    manager.add(window)


with ptg.WindowManager() as manager:
    inputField = ptg.InputField("", prompt="No of rows in square matrix: ")

    window = (
        ptg.Window(
            "",
            inputField,
            "",
            "",
            "",
            ["Submit", lambda *_: noOfRowsSubmit(manager, window)],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]Eigen Values and Eigen Vectors Calculator.")
        .center()
    )

    inputField.bind(ptg.keys.CARRIAGE_RETURN, lambda *_: noOfRowsSubmit(manager, window))
    inputField.bind(ptg.keys.ENTER, lambda *_: noOfRowsSubmit(manager, window))

    manager.add(window)