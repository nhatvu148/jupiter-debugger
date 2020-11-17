import ctypes

def DoOperation(Direction, Name, Text_High, Text_AveSize, Text_MinSize):
    #GUI�̓Ǎ���
    ##Direction = 0 or 1 or 2 #High #Name #AveSize #MinSize
    High = JPT.ConvertFromDocUnit(float(Text_High), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
    AveSize = JPT.ConvertFromDocUnit(float(Text_AveSize), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
    MinSize = JPT.ConvertFromDocUnit(float(Text_MinSize), JPT.UnitType.Unit_Length) # �����̃h�L�������g�P�ʂ��V�X�e���P�ʂɕϊ�
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

if __name__=='__main__':
  Direction = 1
  Name = "Local_Setting_In_UnderSide"
  Text_High = 8
  Text_AveSize = 2
  Text_MinSize = 1
  DoOperation(Direction, Name, Text_High, Text_AveSize, Text_MinSize)