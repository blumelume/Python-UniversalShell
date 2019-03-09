read -p "Input update folder path"
cp $REPLY ~/
mv $REPLY ~/pythonShell

echo "The files can now be found in ~/pythonShell."
echo "You reference this shell by typing import ~/pythonShell at the top of your next python script"
echo
