import ctypes
from pyjdg import *

def DoOperation(dlg):
  Geometry.AdjustHalfCylinder(poslPoint=[], crlFace=[], crCoord=None, nAxisPlane=0, bDivideFace=True, crlPartTarget=[], bMergeEdge=True)
    #GUI�̓Ǎ���
    ##Direction = 0 or 1 or 2 #High #Name #AveSize #MinSize
    Name = dlg.get_item_text('Text_Name')
    Direction = dlg.get_combobox_sel('Comb_Direction')
    High = JPT.ConvertFromDocUnit(float(dlg.get_item_text('Text_High')), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
    AveSize = JPT.ConvertFromDocUnit(float(dlg.get_item_text('Text_AveSize')), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
    MinSize = JPT.ConvertFromDocUnit(float(dlg.get_item_text('Text_MinSize')), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
    print("Direction = " + str(Direction))
    print("High = " + str(High))
    print("Name = " + str(Name))
    print("AveSize = " + str(AveSize))
    print("MinSize = " + str(MinSize))

    #�I���p�[�c�̑S�t�F�[�X��I��
    ##listSelectFace = [6:*] ... �I���t�F�[�XID�̃��X�g
    if [_.id for _ in JPT.GetSelectedParts()] == []:
      ctypes.windll.user32.MessageBoxW(0, "Please select at least 1 part", "ERROR", 0)
    else:
      listSelectFace = [("6:" + str(_.id)) \
                        for part in JPT.GetSelectedPartsCr()[1:-1].split(", ") \
                          for _ in JPT.GetEntitiesByAssociation(JPT.DItemType.BODY, \
                            JPT.AssociateType.AS_FACE, int(part.split(":")[-1]))]

      #�I�����ꂽ�F�[�X�̍ő卂�����w��͈͂Ɋ܂܂��ꍇ�A���[�J���ݒ�̑Ώۃt�F�[�X���X�g�ɒǉ�
      ##listTargetFace = [6:*] ... �Ώۃt�F�[�XID�̃��X�g
      listTargetFace = []
      for cursor in listSelectFace:
          if Direction == 0:
            strCommand = 'EntityInfo({0},"XMAX")'.format(cursor)
          elif Direction == 1:
            strCommand = 'EntityInfo({0},"YMAX")'.format(cursor)
          elif Direction == 2:
            strCommand = 'EntityInfo({0},"ZMAX")'.format(cursor)
          strCoodinate = JPT.Exec(strCommand)

          if float(strCoodinate) <= float(High):
              listTargetFace.append(cursor)

      #�Ώۃt�F�[�X�Ƀ��[�J���ݒ�����s
      strCommand = 'CreateLocalSetting_Face("{0}", '.format(Name) + '{' + \
        '2, 1, {0}, {1}, {2}, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0'.format(str(float(AveSize)), str(float(AveSize)*1.4), str(float(MinSize))) + "}" + \
          ', [{0}], [], [], [], 0:0)'.format(str(','.join(listTargetFace)))
      JPT.Exec(strCommand)

def OnButton_Apply(dlg):
    DoOperation(dlg)

def OnButton_Ok(dlg):
    DoOperation(dlg)

def main():
    dlg=JDGCreator(title="Local Setting in Underside",resizable=True,validation=True)
    dlg.add_groupbox(name="GroupBox1",text="Target Area",layout="Window")
    dlg.add_hlayout(name="Layout2",layout="GroupBox1")
    dlg.add_label(name="Label10",text="Direction",width=100,layout="Layout2")
    dlg.add_combobox(name="Comb_Direction",options=["X","Y","Z"],width=100,layout="Layout2")
    dlg.add_hlayout(name="Layout7",layout="GroupBox1")
    dlg.add_label(name="Label11",text="High",width=100,layout="Layout7")
    dlg.add_textbox(name="Text_High",text="634.0",width=100,layout="Layout7")
    dlg.add_groupbox(name="GroupBox13",text="Local Mesh",layout="Window")
    dlg.add_hlayout(name="Layout14",layout="GroupBox13")
    dlg.add_label(name="Label15",text="Name",width=100,layout="Layout14")
    dlg.add_textbox(name="Text_Name",text="LocalMesh(Under)",width=100,layout="Layout14")
    dlg.add_hlayout(name="Layout18",layout="GroupBox13")
    dlg.add_label(name="Label19",text="Ave Size",width=100,layout="Layout18")
    dlg.add_textbox(name="Text_AveSize",text="30.0",width=100,layout="Layout18")
    dlg.add_hlayout(name="Layout21",layout="GroupBox13")
    dlg.add_label(name="Label22",text="Min Size",width=100,layout="Layout21")
    dlg.add_textbox(name="Text_MinSize",text="0.1",width=100,layout="Layout21")
    dlg.add_part_selector()
    dlg.add_hlayout(name="footer",layout="Window")
    dlg.add_space(orientation="horizontal",layout="footer")
    dlg.add_button(name="ButtonApply",text="Apply",layout="footer")
    dlg.add_button(name="ButtonOk",text="Ok",layout="footer")
    dlg.add_button(name="ButtonCancel",text="Cancel",layout="footer")
    dlg.add_space(orientation="horizontal",layout="footer")

    dlg.on_command("ButtonApply", OnButton_Apply) # ButtonApply��ButtonOK�̏����̓V�X�e���Œ�`�ς�
    dlg.on_command("ButtonOk", OnButton_Ok) # ButtonApply��ButtonOK�̏����̓V�X�e���Œ�`�ς�

    dlg.generate_window()

if __name__=='__main__':
    main()